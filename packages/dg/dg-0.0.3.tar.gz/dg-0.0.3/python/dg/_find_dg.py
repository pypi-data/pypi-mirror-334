from __future__ import annotations

import os
import sys
import sysconfig


def find_dg_bin() -> str:
    """Return the dg binary path."""

    dg_exe = "dg" + sysconfig.get_config_var("EXE")

    path = os.path.join(sysconfig.get_path("scripts"), dg_exe)
    if os.path.isfile(path):
        return path

    if sys.version_info >= (3, 10):
        user_scheme = sysconfig.get_preferred_scheme("user")
    elif os.name == "nt":
        user_scheme = "nt_user"
    elif sys.platform == "darwin" and sys._framework:
        user_scheme = "osx_framework_user"
    else:
        user_scheme = "posix_user"

    path = os.path.join(sysconfig.get_path("scripts", scheme=user_scheme), dg_exe)
    if os.path.isfile(path):
        return path

    # Search in `bin` adjacent to package root (as created by `pip install --target`).
    pkg_root = os.path.dirname(os.path.dirname(__file__))
    target_path = os.path.join(pkg_root, "bin", dg_exe)
    if os.path.isfile(target_path):
        return target_path

    raise FileNotFoundError(path)
