"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from iprm.api.obj.target import Target
from iprm.core.typeflags import CXX, QT, PYBIND11
from iprm.util.dir import Dir
from iprm.util.env import Env
from iprm.util.compiler import MSVC_COMPILER_NAME, CLANG_COMPILER_NAME, GCC_COMPILER_NAME


class CXXTarget(Target):
    STANDARD = 'standard'
    CONFORMANCE = 'conformance'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from iprm.api.obj.project import Project
        self.type_flags |= (CXX | Project.cxx_compiler_flag())
        self.hex_colour = '#00599C'
        self.properties['headers']: dict[Dir, list[str]] = {}
        self.properties['sources']: dict[Dir, list[str]] = {}

    @classmethod
    def default_compiler_name(cls):
        if Env.platform.windows:
            return MSVC_COMPILER_NAME
        elif Env.platform.macos:
            return CLANG_COMPILER_NAME
        elif Env.platform.linux:
            return GCC_COMPILER_NAME
        return None

    @classmethod
    def default_language_properties(cls, **kwargs):
        defaults = {
            cls.STANDARD: '20',
            cls.CONFORMANCE: True,
        }
        for key, value in defaults.items():
            kwargs.setdefault(key, value)
        return kwargs

    def qt(self):
        # TODO: ensure example works with a precompiled qt-based archive, for cmake, archive is reqired to
        #  contain the lib/cmake/Qt6 folder so we can jsut directly use find_package() inst this scenario and
        #  all of qts machine CMake modules. This is why the explicitly tag we're qt so we can branch off
        #  during cmake generation
        self.type_flags |= QT

    def pybind11(self, py_major, py_minor):
        # TODO: do the same/similar branch off and use of mature CMake modules for pybind11, add it to our TypeFlags
        #  enum to allow for this
        self.type_flags |= PYBIND11
        # TODO: Pybind11 Targets should always implicitly depend on/link with python.
        self.properties['python_major_version'] = py_major
        self.properties['python_minor_version'] = py_minor

    def headers(self, header_dir: Dir, *headers):
        if header_dir not in self.properties['headers']:
            self.properties['headers'][header_dir] = []
        self.properties['headers'][header_dir].extend(headers)

    def sources(self, src_dir: Dir, *sources):
        if src_dir not in self.properties['sources']:
            self.properties['sources'][src_dir] = []
        self.properties['sources'][src_dir].extend(sources)
