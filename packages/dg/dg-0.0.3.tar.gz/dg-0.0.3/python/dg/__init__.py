from __future__ import annotations

from ._find_dg import find_dg_bin

__all__ = ("find_dg_bin",)


def __getattr__(attr_name: str) -> object:
    raise AttributeError(f"module `{__name__}` has no attribute `{attr_name}`")
