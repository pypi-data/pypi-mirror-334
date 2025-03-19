from itertools import zip_longest
from iprm.util.env import Env
from iprm.util.dir import CurrentSourceDir
from iprm.gen.gen import Generator
from iprm.load.native import NativeLoader
from iprm.api.obj.project import Project
from iprm.api.obj.subdirectories import SubDirectories
from iprm.api.obj.cxx import CXXTarget
from iprm.api.obj.rust import RustTarget


class CMakeGenerator(Generator):
    name = 'cmake'

    def __init__(self, native_loader: NativeLoader, **kwargs):
        kwargs['build_dir'] = 'build'
        super().__init__(native_loader, **kwargs)

    @property
    def generated_file_name(self):
        return 'CMakeLists.txt'

    @property
    def release_build_type(self):
        return 'Release'

    @classmethod
    def _generate_project(cls, project: Project):
        # TODO: Don't hardcode minimum version, have it as a general config
        #  setting users can put on Object's, useful for scenarios like this where
        #  there is a generator-specific bit of data that is not generalizable to others
        cmake_content = [
            'cmake_minimum_required(VERSION 3.25)',
            '',
            f'project({project.name}',
            '\tVERSION',
            f'\t\t{project.properties.get('version', '0.1.0')}',
        ]
        description = project.properties.get('description', None)
        if description:
            cmake_content.append('\tDESCRIPTION')
            cmake_content.append(f'\t\t"{description}"')
        url = project.properties.get('url', None)
        if url:
            cmake_content.append('\tHOMEPAGE_URL')
            cmake_content.append(f'\t\t"{url}"')

        langs_dict = project.properties.get('languages', {})
        cmake_content_lang = []
        if langs_dict:
            cmake_content.append('\tLANGUAGES')
            langs_list = list(langs_dict.items())
            for (lang_type, lang_props), next_lang in zip_longest(langs_list, langs_list[1:], fillvalue=None):
                suffix = '' if next_lang is None else '\n'
                if lang_type == CXXTarget.__name__:
                    cmake_content.append(f'\t\tCXX{suffix}')
                    standard = lang_props.get(CXXTarget.STANDARD, None)
                    if standard:
                        cmake_content_lang.append(f'set(CMAKE_CXX_STANDARD {standard})')
                        cmake_content_lang.append('set(CMAKE_CXX_STANDARD_REQUIRED True)')
                        cmake_content_lang.append('')
                    comformance = lang_props.get(CXXTarget.CONFORMANCE, None)
                    if comformance:
                        cmake_content_lang.append('if(MSVC)')
                        cmake_content_lang.append('\tadd_compile_options(/Zc:__cplusplus /permissive-)')
                        cmake_content_lang.append('endif()')
                        cmake_content_lang.append('')
                elif lang_type == RustTarget.__name__:
                    pass

        cmake_content.append(f')')
        cmake_content.append('')

        cxx_compiler = project.cxx_compiler
        if cxx_compiler:
            cmake_content.append(f'set(CMAKE_CXX_COMPILER  {cxx_compiler})')
            cmake_content.append('')
        rust_compiler = project.rust_compiler
        if rust_compiler:
            cmake_content.append(f'set(CMAKE_RUST_COMPILER {rust_compiler})')
            cmake_content.append('')

        if cmake_content_lang:
            cmake_content.extend(cmake_content_lang)

        cmake_content.append('enable_testing()')
        cmake_content.append('')

        cmake_content.append('set_property(GLOBAL PROPERTY USE_FOLDERS ON)')
        cmake_content.append('')
        return cmake_content

    @classmethod
    def _generate_subdirectories(cls, subdirs: SubDirectories):
        cmake_content = []
        dir_paths = subdirs.properties.get('directory_paths', [])
        if dir_paths:
            for dir_path in dir_paths:
                cmake_content.append(f'add_subdirectory({dir_path})')
        cmake_content.append('')
        return cmake_content

    @classmethod
    def _generate_cxx(cls, cxx: CXXTarget):
        def add_sources(tgt, key):
            cmake_content_sources = []
            sources_dict = cxx.properties.get(key, {})
            if sources_dict:
                cmake_content_sources.append(f'target_sources({tgt}')
                cmake_content_sources.append(f'\tPRIVATE')
                for src_dir, src_files in sources_dict.items():
                    dir_path = src_dir.path
                    for src_file in src_files:
                        cmake_content_sources.append(f'\t\t{cls.current_src_dir()}/{dir_path}/{src_file}')

                cmake_content_sources.append(')')
            return cmake_content_sources

        target = cxx.name
        cmake_content = []
        if cxx.is_app:
            cmake_content.append(f'add_executable({target})')
        cmake_content.extend(add_sources(target, 'headers'))
        cmake_content.extend(add_sources(target, 'sources'))
        cmake_content.append('')
        return cmake_content

    @classmethod
    def _generate_rust(cls, rust: RustTarget):
        target = rust.name
        manifest_dir, cargo_file = rust.properties.get('manifest')
        manifest_file = f'"{cls.current_src_dir()}/{cargo_file}"' \
            if manifest_dir == CurrentSourceDir() else \
            f'"{cls.current_src_dir()}/{manifest_dir.path.as_posix()}/{cargo_file}"'

        # TODO: For now assumes the output is an executable and main.rs is in it's standard place, allow for
        #  static/shared libs too
        exe_suffix = '.exe' if Env.platform.windows else ''
        cargo_locked = rust.properties.get('cargo_locked', False)
        return [
            'find_program(CARGO_EXECUTABLE cargo REQUIRED)',
            f'set(CARGO_TARGET_DIR {cls.current_bin_dir()})',
            f'set(CARGO_TOML_PATH {manifest_file})',
            f'if(CMAKE_BUILD_TYPE MATCHES "Release|MinSizeRel|RelWithDebInfo")',
            '\tset(CARGO_PROFILE "release")',
            f'\tset(RUST_EXE_PATH ${{CARGO_TARGET_DIR}}/release/{target}{exe_suffix})',
            f'else()',
            '\tset(CARGO_PROFILE "dev")',
            f'\tset(RUST_EXE_PATH ${{CARGO_TARGET_DIR}}/debug/{target}{exe_suffix})',
            f'endif()',
            '',
            'add_custom_command(',
            '\tOUTPUT ${RUST_EXE_PATH}',
            '\tCOMMAND ${CARGO_EXECUTABLE} build',
            '\t\t--manifest-path ${CARGO_TOML_PATH}',
            '\t\t--target-dir ${CARGO_TARGET_DIR}',
            f'\t\t--profile ${{CARGO_PROFILE}}{'\n--locked' if cargo_locked else ''}',
            f'\tWORKING_DIRECTORY {cls.current_src_dir()}',
            '\tDEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/main.rs ${CARGO_TOML_PATH}',
            '\tVERBATIM',
            ')',
            '',
            f'add_custom_target({target} ALL DEPENDS ${{RUST_EXE_PATH}})',
            '',
        ]

    def _order_key(self, obj):
        pass

    @classmethod
    def current_src_dir(cls):
        return '${CMAKE_CURRENT_SOURCE_DIR}'

    @classmethod
    def current_bin_dir(cls):
        return '${CMAKE_CURRENT_BINARY_DIR}'

    @classmethod
    def configure(cls, **kwargs):
        generator = kwargs.get('generator')
        srcdir = kwargs.get('srcdir')
        bindir = kwargs.get('bindir')
        buildtype = kwargs.get('buildtype')
        cmd = [
            'cmake',
            '-G',
            generator,
            '-S',
            srcdir,
            '-B',
            bindir,
            f'-DCMAKE_BUILD_TYPE={buildtype}',
        ]
        return cls._run_command(cmd)

    @classmethod
    def build(cls, **kwargs):
        bindir = kwargs.get('bindir')
        buildtype = kwargs.get('buildtype')
        target = kwargs.get('target', None)
        numproc = kwargs.get('numproc')
        cmd = [
            'cmake',
            '--build',
            bindir,
            '--config',
            buildtype,
            '--parallel',
            cls._num_procs() if numproc is None else numproc
        ]
        if target:
            cmd.extend(['--target', target])
        return cls._run_command(cmd)

    @classmethod
    def test(cls, **kwargs):
        bindir = kwargs.get('bindir')
        buildtype = kwargs.get('buildtype')
        cmd = [
            'ctest',
            '--test-dir',
            bindir,
            '-C',
            buildtype,
        ]
        return cls._run_command(cmd)

    @classmethod
    def install(cls, **kwargs):
        # TODO: impl install
        pass
