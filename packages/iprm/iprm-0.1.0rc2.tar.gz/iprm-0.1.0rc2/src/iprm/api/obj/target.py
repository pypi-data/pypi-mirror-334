"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from iprm.core.object import Object
from iprm.core.typeflags import TARGET, STATIC, SHARED, EXECUTABLE, TEST, MSVC, MSVC_CLANG, CLANG, GCC, RUSTC

class Target(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hex_colour = '#454545'
        self.shape_type = 'box'
        self.type_flags = TARGET
        self.properties['dependencies']: list[str] = []

    def static(self):
        self.type_flags |= STATIC

    def shared(self):
        self.type_flags |= SHARED

    def executable(self):
        self.shape_type = 'ellipse'
        self.type_flags |= EXECUTABLE

    def test(self):
        self.type_flags |= TEST

    def requires(self, *targets):
        self.properties['dependencies'].extend(targets)

    @property
    def dependencies(self):
        return self.properties['dependencies']
