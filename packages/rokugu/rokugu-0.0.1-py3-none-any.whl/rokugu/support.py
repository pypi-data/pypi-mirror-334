import sys
from os import PathLike
from pathlib import Path
from typing import Union

from PySide6.QtCore import QStandardPaths


def bundle_path(path: Union[Path, str] = "") -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).joinpath(path)

    return Path().cwd().joinpath(path)


def standard_path(
    standard_location: QStandardPaths.StandardLocation,
    *other: Union[str, PathLike[str]],
) -> Path:
    path = Path(QStandardPaths.writableLocation(standard_location))
    path.mkdir(parents=True, exist_ok=True)
    return path.joinpath(*other)


def file_size(size_in_bytes: float, precision: int = 2) -> str:
    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    index = 0
    while (size_in_bytes / 1024) > 0.9 and (index < len(units) - 1):
        size_in_bytes /= 1024
        index += 1

    return f"{size_in_bytes:.{precision}f} {units[index]}"
