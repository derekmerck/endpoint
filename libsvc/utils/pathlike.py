import typing as typ
import pathlib

PathLike = typ.Union[str, pathlib.Path]


def mk_path(path: PathLike) -> pathlib.Path:
    path = pathlib.Path(path)
    path = path.expanduser()
    return path
