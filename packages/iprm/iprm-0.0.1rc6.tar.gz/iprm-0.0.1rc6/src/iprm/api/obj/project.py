"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from iprm.util.env import Env
from iprm.core.object import Object
from iprm.core.typeflags import PROJECT
from iprm.api.obj.target import COMPILER
from iprm.api.obj.cxx import CXXTarget
from iprm.api.obj.rust import RustTarget


class Project(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags = PROJECT
        self.hex_colour = '#FFC107'
        self.shape_type = 'star'
        self._root_dir = Env.meta.build_file.parent
        self._cxx_compiler = None
        self._rust_compiler = None

    @property
    def root_dir(self):
        return self._root_dir

    def version(self, version):
        self.properties['version'] = version

    def description(self, description):
        self.properties['description'] = description

    def url(self, url):
        self.properties['url'] = url

    def enable_cxx(self, **kwargs):
        kwargs = CXXTarget.default_language_properties(**kwargs)
        self._cxx_compiler = kwargs.get(COMPILER, None)
        self._enable_language(CXXTarget.__name__, **kwargs)

    @property
    def cxx_compiler(self):
        return self._cxx_compiler

    def enable_rust(self, **kwargs):
        kwargs = RustTarget.default_language_properties(**kwargs)
        self._rust_compiler = kwargs.get(COMPILER, None)
        self._enable_language(RustTarget.__name__, **kwargs)

    @property
    def rust_compiler(self):
        return self._rust_compiler

    def _enable_language(self, language: str, **kwargs):
        if 'languages' not in self.properties:
            self.properties['languages'] = {}
        self.properties['languages'][language] = kwargs
