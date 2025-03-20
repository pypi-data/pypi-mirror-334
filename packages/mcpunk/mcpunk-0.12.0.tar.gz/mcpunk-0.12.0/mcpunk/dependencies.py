# ruff: noqa: E402
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Union

__all__ = [
    "Dependencies",
    "deps",
]


class Singleton(type):
    _instances: dict[Any, Any] = {}  # noqa: RUF012

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class DependencyState:
    settings: Union["Settings", None] = None

    settings_override: Union["Settings", None] = None


class Dependencies(metaclass=Singleton):
    """Dependencies that can play nice with testing.

    If you want to get settings etc. do it here. This means that in
    tests we can patch/etc JUST this object and have everything play nice.
    """

    def __init__(self) -> None:
        self._state = DependencyState()

    def settings(self) -> "Settings":
        if self._state.settings_override is not None:
            return self._state.settings_override
        if self._state.settings is None:
            self._state.settings = Settings()
        return self._state.settings

    @contextmanager
    def override(
        self,
        settings: Union["Settings", None] = None,
        settings_partial: Union["Settings", None] = None,
    ) -> Generator[None, None, None]:
        """Override dependency functions for testing."""
        # Backup current state and methods
        orig_state = self._state

        if settings_partial is not None:
            if settings is not None:
                # heyo maybe an @override 🤷
                raise ValueError("settings and settings_partial cannot both be set")

            if orig_state.settings_override is not None:
                existing_kwargs = orig_state.settings_override.model_dump()
            else:
                existing_kwargs = {}
            new_kwargs = settings_partial.model_dump(exclude_unset=True)
            merged_kwargs = {**existing_kwargs, **new_kwargs}
            settings = Settings(**merged_kwargs)

        # Carry across the overrides, typical use for this is multiple nesting
        # of override contexts managers.
        new_state = DependencyState(
            settings_override=orig_state.settings_override,
        )
        new_state.settings_override = settings
        self._state = new_state

        try:
            yield
        finally:
            self._state = orig_state


from mcpunk.settings import Settings

deps = Dependencies()
