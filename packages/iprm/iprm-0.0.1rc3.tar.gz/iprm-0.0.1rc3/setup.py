import os
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys

root_dir_path = os.path.dirname(__file__)
src_dir_path = os.path.abspath(os.path.join(root_dir_path, 'src', 'iprm', 'util'))
sys.path.append(src_dir_path)


class CMakeExtension(Extension):
    def __init__(self, name):
        Extension.__init__(self, name, sources=[])


class IPRMBuild(build_ext):
    def run(self):
        try:
            subprocess.check_output(['ninja', '--version'])
        except OSError:
            raise RuntimeError("Ninja must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        if isinstance(ext, CMakeExtension):
            import platform
            configure = [
                'cmake',
                '-G', 'Ninja',
                '-S', '.',
                '-B', 'build_pkg',
                '-DCMAKE_BUILD_TYPE=RelWithDebInfo',
                '-DIPRM_INCLUDE_STUDIO_RUST_IMPL=FALSE',
                '-DIPRM_INCLUDE_STUDIO_WEB_IMPL=FALSE',
            ]
            if platform.system() == 'Darwin':
                # TODO: Don't hard code the macOS Qt install, just like windows, create a PLATFORM-macos
                #  section with a precompiled portion, only containined the Qt modules we need (Core, GUi, Widgets,
                #  and Svg) to keep the git LFS light
                configure.append('-DCMAKE_PREFIX_PATH=~/qt/6.8.2/macos/lib/cmake/Qt6')
            build = [
                'cmake',
                '--build', 'build_pkg',
                '--config', 'RelWithDebInfo',
                '--parallel',
                '--verbose',
                '--target',
                'core'
            ]
            src_dir = os.path.abspath(os.path.join('src', 'iprm'))
            from vcvarsall import vcvarsall_script
            if platform.system() == "Windows":
                subprocess.check_call(vcvarsall_script(' '.join(configure)), cwd=src_dir)
                subprocess.check_call(vcvarsall_script(' '.join(build)), cwd=src_dir)
            else:
                subprocess.check_call(configure, cwd=src_dir)
                subprocess.check_call(build, cwd=src_dir)
            install = [
                'cmake',
                '--install', 'build_pkg',
                '--config', 'RelWithDebInfo',
            ]
            # subprocess.check_call(' '.join(install), cwd=src_dir)


setup(
    ext_modules=[CMakeExtension("IPRM Core and Extension Modules"), ],
    cmdclass={"build_ext": IPRMBuild},
)
