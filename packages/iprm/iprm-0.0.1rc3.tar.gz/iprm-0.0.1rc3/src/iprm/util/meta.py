from contextlib import contextmanager
from pathlib import Path
from typing import Optional

_current_build_file: Optional[Path] = None


@contextmanager
def meta_context(build_file: Path):
    global _current_build_file
    previous_context = _current_build_file
    _current_build_file = build_file
    try:
        yield
    finally:
        _current_build_file = previous_context


class Meta:
    def __init__(self):
        global _current_build_file
        self.build_file: Path = _current_build_file.resolve() if _current_build_file is not None else None
