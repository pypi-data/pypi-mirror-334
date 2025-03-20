import inspect
import json
import logging
import pathlib
import textwrap
from collections.abc import Sequence
from typing import Annotated, Any, Literal, Self, assert_never

import mcp.types as mcp_types
from fastmcp import FastMCP
from git import Repo
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)
from pydantic_core import to_jsonable_python

from mcpunk.dependencies import deps
from mcpunk.file_breakdown import (
    File,
)
from mcpunk.file_breakdown import (
    Project as FileBreakdownProject,
)
from mcpunk.file_chunk import Chunk
from mcpunk.git_analysis import get_recent_branches
from mcpunk.util import create_file_tree, log_inputs_outputs

logger = logging.getLogger(__name__)

PROJECTS: dict[str, "ToolProject"] = {}


mcp = FastMCP("Code Analysis")

ToolResponseSingleItem = mcp_types.TextContent | mcp_types.ImageContent | mcp_types.EmbeddedResource
ToolResponseSequence = Sequence[ToolResponseSingleItem]
ToolResponse = ToolResponseSequence | ToolResponseSingleItem
FilterType = Annotated[
    str | list[str] | None,
    Field(
        description=(
            "Match if any of these strings appear. Match all if None/null. "
            "Single empty string or empty list will match all."
        ),
    ),
]


class ToolProject(BaseModel):
    """A project containing files split into chunks and so on.

    These are created by the `configure_project` tool, and can be referenced by name
    (which is the key in the `PROJECTS` global dict) when calling other tools.
    """

    chunk_project: FileBreakdownProject

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def root(self) -> pathlib.Path:
        return self.chunk_project.root

    @property
    def git_path(self) -> pathlib.Path:
        if str(self.root).endswith(".git"):
            git_dir_path = self.root
        else:
            git_dir_path = self.root / ".git"
        if not git_dir_path.exists():
            raise ValueError(f"git dir not found at {git_dir_path}")
        return git_dir_path


class ProjectFile(BaseModel):
    project_name: str
    rel_path: Annotated[pathlib.Path, Field(description="Relative to project root")]

    @property
    def project(self) -> ToolProject:
        return _get_project_or_error(self.project_name)

    @property
    def abs_path(self) -> pathlib.Path:
        return self.project.chunk_project.root / self.rel_path

    @property
    def file(self) -> File:
        abs_path = self.abs_path
        matching_files = [f for f in self.project.chunk_project.files if f.abs_path == abs_path]
        if len(matching_files) != 1:
            raise ValueError(f"File {self.abs_path} not found in project {self.project_name}")
        return matching_files[0]

    @model_validator(mode="after")
    def validate_misc(self) -> Self:
        assert self.project is not None
        assert self.file is not None
        return self


class MCPToolOutput(BaseModel):
    """The output of a tool.

    You can specify any of the items in here, and they will all be rendered and
    returned to the client. If you specify NOTHING then the default response
    will be returned.
    """

    is_error: bool = False
    # Anything that pydantic core to_jsonable_python can handle - that's a lot of stuff!
    jsonable: Any | None = None
    raw: ToolResponse | None = None
    text: str | None = None

    # You might like this set to 2/4 for debugging, makes things look nice!
    # But that means more token usage I guess.
    # an int will do what you expect. None for compact. If unset, will default to
    # the value from settings.
    indent: int | Literal["no_indent"] = Field(
        default_factory=lambda: deps.settings().default_response_indent,
    )

    default_response: str = "No response provided. This is not an error."

    # If the sum of the length of all text responses is greater than this
    # then an error will be returned to the caller. non-text responses (image, etc)
    # are not counted.
    max_chars: int = Field(
        default_factory=lambda: deps.settings().default_response_max_chars,
    )

    # Whether to include the number of characters in the response in the response.
    # So like `[DEBUG INFO: Response is 1234 chars]` prefixed to the response.
    include_chars_in_response: bool = Field(
        default_factory=lambda: deps.settings().include_chars_in_response,
    )

    def render(self) -> ToolResponse:
        indent: int | None
        if self.indent == "no_indent":
            indent = None
        elif isinstance(self.indent, int):
            assert isinstance(self.indent, int)
            indent = self.indent
        else:
            assert_never(self.indent)
        assert indent is None or isinstance(indent, int)

        out: list[ToolResponseSingleItem] = []
        if self.is_error:
            out.append(mcp_types.TextContent(type="text", text="An error occurred."))
        if self.jsonable is not None:
            logger.debug(
                "Jsonable response\n"
                + textwrap.indent(json.dumps(to_jsonable_python(self.jsonable), indent=2), "    "),
            )
            out.append(
                mcp_types.TextContent(
                    type="text",
                    text=json.dumps(to_jsonable_python(self.jsonable), indent=indent),
                ),
            )
        if self.raw is not None:
            if isinstance(self.raw, ToolResponseSingleItem):
                out.append(self.raw)
            elif isinstance(self.raw, Sequence):
                assert all(isinstance(x, ToolResponseSingleItem) for x in self.raw)
                out.extend(self.raw)
            else:
                assert_never(self.raw)
        if self.text is not None:
            out.append(mcp_types.TextContent(type="text", text=self.text))
        if len(out) == 0:
            # Use default response if no data was provided
            assert not self.is_error  # Don't want to say there's an error if there was!
            out.append(mcp_types.TextContent(type="text", text=self.default_response))

        total_chars = sum(len(x.text) for x in out if isinstance(x, mcp_types.TextContent))
        if total_chars > self.max_chars:
            msg = (
                f"Response is {total_chars} chars which exceed the maximum allowed "
                f"of {self.max_chars}. Please adjust your request and try again."
            )
            logger.warning(msg)
            out = [mcp_types.TextContent(type="text", text=msg)]

        if self.include_chars_in_response:
            len_msg = f"[DEBUG INFO: Response is {total_chars} chars]"
            if len(out) == 1 and isinstance(out[0], mcp_types.TextContent):
                out[0].text = f"{len_msg}\n\n{out[0].text}"
            else:
                out.insert(
                    0,
                    mcp_types.TextContent(type="text", text=f"Response is {total_chars} chars"),
                )

        final_out: ToolResponse
        if len(out) == 1:
            final_out = out[0]
        else:
            final_out = out
        # logger.debug(f"Response {final_out}")
        logger.debug(
            "Final response\n"
            + textwrap.indent(json.dumps(to_jsonable_python(final_out), indent=2), "    "),
        )
        return final_out


@mcp.tool()
@log_inputs_outputs()
def get_a_joke(animal: Annotated[str, Field(max_length=20)]) -> ToolResponse:
    """Get a really funny joke! For testing :)"""
    return MCPToolOutput(
        text=(
            f"Why did the {animal} cross the road?\n"
            f"To get to the other side!\n"
            f"Because it was a {animal}."
        ),
    ).render()


@mcp.tool()
@log_inputs_outputs()
def configure_project(
    root_path: Annotated[pathlib.Path, Field(description="Root path of the project")],
    project_name: Annotated[
        str,
        Field(
            description=(
                "Name of the project, for you to pick buddy, "
                "something short and sweet and memorable and unique"
            ),
        ),
    ],
) -> ToolResponse:
    """Configure a new project containing files.

    Each file in the project is split into 'chunks' - logical sections like functions,
    classes, markdown sections, and import blocks.

    After configuring, a common workflow is:
    1. list_all_files_in_project to get an overview of the project (with
       an initial limit on the depth of the search)
    2. Find files by function/class definition:
       find_files_by_chunk_content(... ["def my_funk"])
    3. Find files by function/class usage:
       find_files_by_chunk_content(... ["my_funk"])
    4. Determine which chunks in the found files are relevant:
        find_matching_chunks_in_file(...)
    5. Get details about the chunks:
       chunk_details(...)

    Use ~ (tilde) literally if the user specifies it in paths.
    """
    path = root_path.expanduser().absolute()
    if project_name in PROJECTS:
        raise ValueError(f"Project {project_name} already exists")
    project = ToolProject(
        chunk_project=FileBreakdownProject(
            root=path,
            file_watch_refresh_freq_seconds=deps.settings().file_watch_refresh_freq_seconds,
            max_chunk_size=deps.settings().max_chunk_size,
        ),
    )
    PROJECTS[project_name] = project
    return MCPToolOutput(
        text=(
            inspect.cleandoc(f"""\
            Project {path} configured with {len(project.chunk_project.files)} files.
            Files are split into 'chunks' - logical sections like:
            - Functions (e.g. 'def my_function')
            - Classes (e.g. 'class MyClass')
            - Markdown sections (e.g. '# Section')
            - Import blocks

            After configuring, a common workflow is:
            1. list_all_files_in_project to get an overview of the project (with
               an initial limit on the depth of the search)
            2. Find files by function/class definition:
               find_files_by_chunk_content(... ["def my_funk"])
            3. Find files by function/class usage:
               find_files_by_chunk_content(... ["my_funk"])
            4. Determine which chunks in the found files are relevant:
                find_matching_chunks_in_file(...)
            5. Get details about the chunks:
               chunk_details(...)

            Do not immediately list files or otherwise use the project
            unless explicitly told to do so.
        """)
        ),
    ).render()


@mcp.tool()
@log_inputs_outputs()
def list_all_files_in_project(
    project_name: str,
    path_filter: FilterType = None,
    limit_depth_from_root: Annotated[
        int | None,
        Field(
            description=(
                "Limit the depth of the search to this many directories from the root. "
                "Typically,start with 1 to get an overview of the project."
                "If None, search all directories from the root."
            ),
        ),
    ] = None,
) -> ToolResponse:
    """List all files in a project, returning a file tree.

    This is useful for getting an overview of the project, or specific
    subdirectories of the project.

    A project may have many files, so you are suggested
    to start with a depth limit to get an overview, and then continue increasing
    the depth limit with a filter to look at specific subdirectories.
    """
    project = _get_project_or_error(project_name)
    data = create_file_tree(
        project_root=project.root,
        paths={x.abs_path for x in project.chunk_project.files},
        limit_depth_from_root=limit_depth_from_root,
        filter_=path_filter,
    )
    if data is None:
        return MCPToolOutput(text="No paths").render()
    elif isinstance(data, str):
        return MCPToolOutput(text=data).render()
    else:
        assert_never(data)


@mcp.tool()
@log_inputs_outputs()
def find_files_by_chunk_content(
    project_name: str,
    chunk_contents_filter: FilterType,
) -> ToolResponse:
    """Step 1: Find files containing chunks with matching text.

    Returns file tree only showing which files contain matches.
    You must use find_matching_chunks_in_file on each relevant file
    to see the actual matches.

    Example workflow:
    1. Find files:
       files = find_files_by_chunk_content(project, ["MyClass"])
    2. For each file, find actual matches:
       matches = find_matching_chunks_in_file(file, ["MyClass"])
    3. Get content:
       content = chunk_details(file, match_id)
    """
    return _filter_files_by_chunk(project_name, chunk_contents_filter, "name_or_content").render()


@mcp.tool()
@log_inputs_outputs()
def find_matching_chunks_in_file(
    project_name: str,
    rel_path: Annotated[pathlib.Path, Field(description="Relative to project root")],
    filter_: FilterType,
) -> ToolResponse:
    """Step 2: Find the actual matching chunks in a specific file.

    Required after find_files_by_chunk_content or list_all_files_in_project to see
    matches, as those tools only show files, not their contents.

    This can be used for things like:
      - Finding all chunks in a file that make reference to a specific function
        (e.g. find_matching_chunks_in_file(..., ["my_funk"])
      - Finding a chunk where a specific function is defined
        (e.g. find_matching_chunks_in_file(..., ["def my_funk"])

    Some chunks are split into multiple parts, because they are too large. This
    will look like 'chunkx_part1', 'chunkx_part2', ...
    """
    proj_file = ProjectFile(project_name=project_name, rel_path=rel_path)
    return _list_chunks_in_file(proj_file, filter_, "name_or_content").render()


@mcp.tool()
@log_inputs_outputs()
def chunk_details(
    chunk_id: str,
) -> ToolResponse:
    """Get full content of a specific chunk.

    Returns chunk content as string.

    Common patterns:
    1. Final step after find_matching_chunks_in_file finds relevant chunks
    2. Examining implementations after finding definitions/uses
    """
    # Yeah this is an awful brute force "search" - if it is even deserving of the
    # name "search"! Ah well.
    the_chunk: Chunk | None = None
    for project in PROJECTS.values():
        for file in project.chunk_project.files:
            for chunk in file.chunks:
                if chunk.id_(file.abs_path) == chunk_id:
                    the_chunk = chunk
                    break

    if the_chunk is None:
        return MCPToolOutput(
            text="No matching chunks. Please use other tools to find available chunks.",
        ).render()
    return MCPToolOutput(text=inspect.cleandoc(the_chunk.content)).render()


@mcp.tool()
@log_inputs_outputs()
def list_most_recently_checked_out_branches(
    project_name: str,
    n: Annotated[int, Field(ge=20, le=50)] = 20,
) -> ToolResponse:
    """List the n most recently checked out branches in the project"""
    project = _get_project_or_error(project_name)
    return MCPToolOutput(text="\n".join(get_recent_branches(project.git_path, n))).render()


@mcp.tool()
@log_inputs_outputs()
def diff_with_ref(
    project_name: str,
    ref: Annotated[str, Field(max_length=100)],
) -> ToolResponse:
    """Return a summary of the diff between HEAD and the given ref.

    You probably want the ref  to be the 'base' branch like develop or main, off which
    PRs are made - and you can likely determine this by viewing the most recently
    checked out branches.
    """
    project = _get_project_or_error(project_name)
    repo = Repo(project.git_path)
    # head = repo.head.commit
    # compare_from = repo.commit(ref)
    # diffs = compare_from.diff(head, create_patch=True)
    # print(repo.git.diff(f"{ref}s...HEAD", ignore_blank_lines=True, ignore_space_at_eol=True))
    diff = repo.git.diff(
        f"{ref}...HEAD",
        ignore_blank_lines=True,
        ignore_space_at_eol=True,
    )
    return MCPToolOutput(
        text=diff,
        max_chars=deps.settings().default_git_diff_response_max_chars,
    ).render()


def _get_project_or_error(project_name: str) -> ToolProject:
    if project_name not in PROJECTS:
        raise ValueError(
            f"Project {project_name} not configured. Either double check the project name "
            f"or run the tool to set up a new project. The server may have been restarted "
            f"causing it to no longer be configured.",
        )
    return PROJECTS[project_name]


def _list_chunks_in_file(
    proj_file: ProjectFile,
    filter_: FilterType,
    filter_on: Literal["name", "name_or_content"],
) -> MCPToolOutput:
    target_file = proj_file.file
    chunks = [x for x in target_file.chunks if x.matches_filter(filter_, filter_on)]
    resp_data = [
        f"id={x.id_(path=target_file.abs_path)} (category={x.category} chars={len(x.content)})"
        for x in chunks
    ]
    resp_text = "\n".join(resp_data)
    chunk_info = f"({len(chunks)} of {len(target_file.chunks)} chunks)"
    return MCPToolOutput(text=f"{chunk_info}\n{resp_text}")


def _filter_files_by_chunk(
    project_name: str,
    filter_: FilterType,
    filter_on: Literal["name", "name_or_content"],
) -> MCPToolOutput:
    project = _get_project_or_error(project_name)
    matching_files: set[pathlib.Path] = set()
    for file in project.chunk_project.files:
        if any(c.matches_filter(filter_, filter_on) for c in file.chunks):
            matching_files.add(file.abs_path)
    data = create_file_tree(project_root=project.root, paths=matching_files)
    if data is None:
        return MCPToolOutput(text="No files found")
    elif isinstance(data, str):
        return MCPToolOutput(text=data)
    else:
        assert_never(data)


if __name__ == "__main__":
    import time

    t1 = time.monotonic()
    configure_project(
        root_path=pathlib.Path("~/git/mcpunk"),
        project_name="mcpunk",
    )
    t2 = time.monotonic()
    print(f"Configured project in {(t2 - t1) * 1000:.2f}ms")
    _proj = PROJECTS["mcpunk"].chunk_project
    print(len([f for f in _proj.files if f.ext == ".py"]), "files")
    print(sum(len(f.contents.splitlines()) for f in _proj.files if f.ext == ".py"), "lines")
    print(sum(len(f.contents) for f in _proj.files if f.ext == ".py"), "chars")
    find_files_by_chunk_content(
        project_name="mcpunk",
        chunk_contents_filter=["desktop"],
    )
    _list_chunks_in_file(
        proj_file=ProjectFile(
            project_name="mcpunk",
            rel_path=pathlib.Path("README.md"),
        ),
        filter_=None,
        filter_on="name",
    )
    chunk_details(chunk_id="xxx")
    # f = [
    #     x
    #     for x in PROJECTS["mcpunk"].chunk_project.files
    #     if x.abs_path == pathlib.Path(PROJECTS["mcpunk"].root / "docs/infrastructure.md")
    # ][0]
    diff_with_ref(
        project_name="mcpunk",
        ref="main",
    )
