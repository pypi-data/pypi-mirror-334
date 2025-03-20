"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from contextlib import contextmanager
from typing import Optional, List, Any
from typeflags import TypeFlags


@contextmanager
def object_created_callback(on_object_created: callable): ...


class Object:
    properties: dict[str, Any]

    def __init__(self, name: str) -> None: ...

    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, value: str) -> None: ...

    @property
    def type_flags(self) -> TypeFlags: ...

    @type_flags.setter
    def type_flags(self, value: TypeFlags) -> None: ...

    @property
    def dependencies(self) -> List[str]: ...

    @dependencies.setter
    def dependencies(self, value: List[str]) -> None: ...

    @property
    def hex_colour(self) -> Optional[str]: ...

    @hex_colour.setter
    def hex_colour(self, value: Optional[str]) -> None: ...

    @property
    def shape_type(self) -> str: ...

    @shape_type.setter
    def shape_type(self, value: str) -> None: ...

    @property
    def shape_num_sides(self) -> Optional[int]: ...

    @shape_num_sides.setter
    def shape_num_sides(self, value: Optional[int]) -> None: ...

    # Read-only type flag properties
    @property
    def is_project(self) -> bool: ...

    @property
    def is_subdirs(self) -> bool: ...

    @property
    def is_target(self) -> bool: ...

    @property
    def is_test(self) -> bool: ...

    @property
    def is_app(self) -> bool: ...

    @property
    def is_lib(self) -> bool: ...

    @property
    def is_header(self) -> bool: ...

    @property
    def is_static(self) -> bool: ...

    @property
    def is_shared(self) -> bool: ...

    @property
    def is_native_pkg(self) -> bool: ...

    @property
    def is_pkg_config(self) -> bool: ...

    @property
    def is_precompiled(self) -> bool: ...

    @property
    def is_source(self) -> bool: ...

    @property
    def is_archive(self) -> bool: ...

    @property
    def is_framework(self) -> bool: ...

    @property
    def is_container(self) -> bool: ...

    @property
    def is_static_crt(self) -> bool: ...

    @property
    def is_dynamic_crt(self) -> bool: ...

    @property
    def is_dual_crt(self) -> bool: ...

    @property
    def is_cxx(self) -> bool: ...

    @property
    def is_rust(self) -> bool: ...

    @property
    def is_qt(self) -> bool: ...

    @property
    def is_pybind11(self) -> bool: ...
