from iprm.api.obj.target import Target, COMPILER, COMPILER_DESC, available_unix_compilers, available_windows_compilers
from iprm.core.typeflags import CXX, QT
from iprm.util.dir import Dir
from iprm.util.env import Env
from iprm.util.vcvarsall import find_vcvarsall

MSVC = 'cl'
MSVC_CLANG = 'clang-cl'
GCC = 'g++'
CLANG = 'clang++'

UNIX_COMPILERS = (GCC, CLANG)
WINDOWS_COMPILERS = (MSVC, MSVC_CLANG) + UNIX_COMPILERS
SUPPORTED_COMPILERS = WINDOWS_COMPILERS if Env.platform.windows else UNIX_COMPILERS


class CXXTarget(Target):
    STANDARD = 'standard'
    CONFORMANCE = 'conformance'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= CXX
        self.properties['headers']: dict[Dir, list[str]] = {}
        self.properties['sources']: dict[Dir, list[str]] = {}


    def qt(self):
        # TODO: ensure example works with a precompiled qt-based archive, for cmake, archive is reqired to
        #  contain the lib/cmake/Qt6 folder so we can jsut directly use find_package() inst this scenario and
        #  all of qts machine CMake modules. This is why the explicitly tag we're qt so we can branch off
        #  during cmake generation
        self.type_flags |= QT

    # TODO: do the same/similar branch off and use of mature CMake modules for pybind11, add it to our TypeFlags
    #  enum to allow for this


    def headers(self, header_dir: Dir, *headers):
        if header_dir not in self.properties['headers']:
            self.properties['headers'][header_dir] = []
        self.properties['headers'][header_dir].extend(headers)

    def sources(self, src_dir: Dir, *sources):
        if src_dir not in self.properties['sources']:
            self.properties['sources'][src_dir] = []
        self.properties['sources'][src_dir].extend(sources)

    @classmethod
    def default_language_properties(cls, **kwargs):
        defaults = {
            cls.STANDARD: '20',
            cls.CONFORMANCE: True,
        }
        # TODO: This should be invoked on the IPRM configure command
        #defaults.update(cls._default_compiler_properties(**kwargs))
        for key, value in defaults.items():
            kwargs.setdefault(key, value)
        return kwargs

    @classmethod
    def _default_compiler(cls):
        compilers = cls._available_compilers()
        if Env.platform.windows and MSVC in compilers:
            return MSVC, compilers[MSVC]
        elif Env.platform.macos and CLANG in compilers:
            return CLANG, compilers[CLANG]
        elif Env.platform.linux and GCC in compilers:
            return GCC, compilers[GCC]
        return None

    @classmethod
    def _available_compilers(cls):
        cpp_info = {}
        if Env.platform.windows:
            if find_vcvarsall():
                cpp_info.update({
                    MSVC: {
                        'version_command': f'{MSVC} 2>&1',
                        'version_parse_callback': cls._parse_cl_version_output,
                        'requires_vcvarsall': True,
                    },
                    MSVC_CLANG: {
                        'version_command': f'{MSVC_CLANG} --version',
                        'version_parse_callback': cls._parse_clang_version_output,
                        'requires_vcvarsall': True,
                    },
                })

            cpp_info.update({
                GCC: {
                    'version_command': f'{GCC} --version',
                    'parse_callback': cls._parse_gcc_version_output,
                },
                CLANG: {
                    'version_command': f'{CLANG} --version',
                    'parse_callback': cls._parse_clang_version_output,
                },
            })
            return available_windows_compilers(cpp_info)
        else:
            cpp_info.update({
                GCC: {
                    'version_command': f'{GCC} --version',
                    'parse_callback': cls._parse_gcc_version_output,
                },
                CLANG: {
                    'version_command': f'{CLANG} --version',
                    'parse_callback': cls._parse_clang_version_output,
                },
            })
            return available_unix_compilers(cpp_info)

    @staticmethod
    def _parse_gcc_version_output(output: str) -> str:
        lines = []
        for line in output.split("\n"):
            if line.strip() and not line.startswith("###"):
                lines.append(line)
            elif line.startswith("###"):
                break
        return "\n".join(lines).strip()

    @staticmethod
    def _parse_clang_version_output(output: str) -> str:
        lines = output.strip().split("\n")
        for i, line in enumerate(lines):
            if "clang version" in line:
                return "\n".join(lines[i:i + 4]).strip()
        return output.strip()

    @staticmethod
    def _parse_cl_version_output(output: str) -> str:
        output_lines = output.strip().split("\n")
        return "\n".join(output_lines[:2]).strip()
