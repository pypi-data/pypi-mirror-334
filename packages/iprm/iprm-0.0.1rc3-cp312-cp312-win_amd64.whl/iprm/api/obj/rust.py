from iprm.api.obj.target import Target, COMPILER, COMPILER_DESC, available_unix_compilers, available_windows_compilers
from iprm.core.typeflags import RUST
from iprm.util.dir import Dir
from iprm.util.env import Env

RUSTC = 'rustc'


# TODO: Support gcc-rust when its mature enough: https://rust-gcc.github.io/


class RustTarget(Target):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= RUST
        self.properties['manifest']: tuple[Dir, str] = None
        self.properties['cargo_locked']: bool = None

    # TODO: Support direct/manual rust complication (via the actual rust compiler) instead of forcing cargo infra
    def crate(self, manifest_dir: Dir, cargo_file: str, locked: bool = False):
        self.properties['manifest'] = (manifest_dir, cargo_file)
        self.properties['cargo_locked'] = locked

    @classmethod
    def default_language_properties(cls, **kwargs):
        defaults = {}
        # TODO: This should be invoked on the IPRM configure command
        #defaults.update(cls._default_compiler_properties(**kwargs))
        for key, value in defaults.items():
            kwargs.setdefault(key, value)
        return kwargs

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
