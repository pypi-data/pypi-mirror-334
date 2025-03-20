"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from iprm.api.obj.target import Target
from iprm.core.typeflags import RUST, RUSTC
from iprm.util.dir import Dir

"""
RUSTC = 'rustc'
"""


# TODO: Support gcc-rust when its mature enough: https://rust-gcc.github.io/


class RustTarget(Target):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= (RUST | RUSTC)
        self.hex_colour = '#FF9800'
        self.properties['manifest']: tuple[Dir, str] = None
        self.properties['cargo_locked']: bool = None
        self.properties['sources']: dict[Dir, list[str]] = {}

    # TODO: Support direct/manual rust complication (via the actual rust compiler) instead of forcing cargo infra
    def crate(self, manifest_dir: Dir, cargo_file: str, locked: bool = False):
        self.shape_type = 'ellipse'
        self.properties['manifest'] = (manifest_dir, cargo_file)
        self.properties['cargo_locked'] = locked

    def sources(self, src_dir: Dir, *sources):
        if src_dir not in self.properties['sources']:
            self.properties['sources'][src_dir] = []
        self.properties['sources'][src_dir].extend(sources)

    @classmethod
    def default_language_properties(cls, **kwargs):
        defaults = {}
        for key, value in defaults.items():
            kwargs.setdefault(key, value)
        return kwargs

    # TODO: This is an expensive operation, should only use when Validation support is added, as we'll know if
    #  the user actually has the compiler available or not

    # TODO: Also use this for IPRM Studio properties view
    """
    @classmethod
    def _default_compiler(cls):
        compilers = cls._available_compilers()
        if RUSTC in compilers:
            return RUSTC, compilers[RUSTC]
        return None

    @classmethod
    def _available_compilers(cls):
        if Env.platform.windows:
            rust_info = {
                RUSTC: {
                    'version_command': f'{RUSTC} --version',
                },
            }
            return available_windows_compilers(rust_info)
        else:
            rust_info = {
                RUSTC: {
                    'version_command': f'{RUSTC} --version',
                },
            }
            return available_unix_compilers(rust_info)
    """
