"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from enum import IntFlag
from typing import ClassVar


class TypeFlags(IntFlag):
    NONE: ClassVar[TypeFlags]
    PROJECT: ClassVar[TypeFlags]
    SUBDIRS: ClassVar[TypeFlags]
    TARGET: ClassVar[TypeFlags]
    TEST: ClassVar[TypeFlags]
    EXECUTABLE: ClassVar[TypeFlags]
    LIBRARY: ClassVar[TypeFlags]
    HEADER: ClassVar[TypeFlags]
    STATIC: ClassVar[TypeFlags]
    SHARED: ClassVar[TypeFlags]
    NATIVEPKG: ClassVar[TypeFlags]
    PKGCONFIG: ClassVar[TypeFlags]
    PRECOMPILED: ClassVar[TypeFlags]
    SOURCE: ClassVar[TypeFlags]
    ARCHIVE: ClassVar[TypeFlags]
    FRAMEWORK: ClassVar[TypeFlags]
    CONTAINER: ClassVar[TypeFlags]
    CRTSTATIC: ClassVar[TypeFlags]
    CRTDYNAMIC: ClassVar[TypeFlags]
    CRTDUAL: ClassVar[TypeFlags]
    CXX: ClassVar[TypeFlags]
    RUST: ClassVar[TypeFlags]
    QT: ClassVar[TypeFlags]
    PYBIND11: ClassVar[TypeFlags]
    MSVC: ClassVar[TypeFlags]
    MSVC_CLANG: ClassVar[TypeFlags]
    CLANG: ClassVar[TypeFlags]
    GCC: ClassVar[TypeFlags]
    RUSTC: ClassVar[TypeFlags]

    def __or__(self, other: TypeFlags) -> TypeFlags: ...

    def __and__(self, other: TypeFlags) -> TypeFlags: ...

    def __invert__(self) -> TypeFlags: ...

    def __int__(self) -> int: ...


# Export all enum values at module level
NONE: TypeFlags
PROJECT: TypeFlags
SUBDIRS: TypeFlags
TARGET: TypeFlags
TEST: TypeFlags
EXECUTABLE: TypeFlags
LIBRARY: TypeFlags
HEADER: TypeFlags
STATIC: TypeFlags
SHARED: TypeFlags
NATIVEPKG: TypeFlags
PKGCONFIG: TypeFlags
PRECOMPILED: TypeFlags
SOURCE: TypeFlags
ARCHIVE: TypeFlags
FRAMEWORK: TypeFlags
CONTAINER: TypeFlags
CRTSTATIC: TypeFlags
CRTDYNAMIC: TypeFlags
CRTDUAL: TypeFlags
CXX: TypeFlags
RUST: TypeFlags
QT: TypeFlags
PYBIND11: TypeFlags
MSVC: TypeFlags
MSVC_CLANG: TypeFlags
CLANG: TypeFlags
GCC: TypeFlags
RUSTC: TypeFlags
