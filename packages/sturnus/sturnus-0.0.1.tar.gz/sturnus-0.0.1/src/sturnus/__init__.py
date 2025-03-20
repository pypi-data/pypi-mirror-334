from typing import Iterable

__path__: Iterable[str] = __import__(name="pkgutil").extend_path(
    __path__,
    __name__,
)
