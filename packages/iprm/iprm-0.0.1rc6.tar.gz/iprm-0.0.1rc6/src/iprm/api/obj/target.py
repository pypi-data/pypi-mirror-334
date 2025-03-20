"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import os
import sys
import tempfile
import subprocess
from typing import Dict, List, Any
from iprm.core.object import Object
from iprm.core.typeflags import TARGET, STATIC, SHARED, EXECUTABLE, TEST
from iprm.util.env import Env
from iprm.util.vcvarsall import find_vcvarsall

COMPILER = 'compiler'
COMPILER_DESC = 'compiler_description'


# TODO: We should have some "target specific compiler options" API should be exposed for low level
#  projects that get very specific, especially across platforms. Should
#  also have the same for global vs local preprocessor defines. If a generator doesn't support target-specific
#  compilers natively (not through hacks like custom targets/commands), then we will just ignore any attempt at
#  target-specific compilers and use global/project level compiler. Users can build their own custom targets like
#  they would have to do in that project model anyways
#
# TODO: We'll use the above infrastructure to show an icon for each target. cl and clang-cl will use the Visual Studio
#  Icon, GCC use its Icon, clang use the LLVM icon (since Mingw is a thing, Windows can display theses too), and Rust
#  uses the Rust icon

# TODO: Pybind11 Targets should always implicitly depend on/link with python. Their API should allow them to
#  specify the version
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

    @classmethod
    def _default_compiler_properties(cls, **kwargs):
        defaults = {}
        compiler_name = kwargs.get(COMPILER, None)
        if compiler_name:
            # While description is nice to have, most users probably won't care about setting this,
            # so don't require the expensive default call if compiler is specified but description
            # is not, only vice versa will require the default compiler detection
            compiler_dec = kwargs.get(COMPILER_DESC, '')
            defaults[COMPILER] = compiler_name
            defaults[COMPILER_DESC] = compiler_dec
        else:
            compiler_name, compiler_dec = cls._default_compiler()
            defaults[COMPILER] = compiler_name
            defaults[COMPILER_DESC] = compiler_dec
        return defaults


# TODO: Expose this on the CLI as a query result, also in Studio display the defualt of the targets compiler by
#  invoking this
def available_windows_compilers(compiler_info: Dict[str, Dict[str, Any]]):
    batch_script = ["@echo off"]
    vcvarsall_path = find_vcvarsall()

    if vcvarsall_path is not None:
        batch_script.extend([
            f'echo ###VCVARSALL_FOUND###',
            f'call "{vcvarsall_path}" x64'
        ])
    else:
        batch_script.append(f'echo ###VCVARSALL_NOT_FOUND###')

    batch_script.append('echo ###BEGIN_COMPILER_CHECK###')

    for compiler, info in compiler_info.items():
        compiler_upper = compiler.upper()
        available_marker = f'{compiler_upper}_AVAILABLE'
        not_available_marker = f'{compiler_upper}_NOT_AVAILABLE'
        check_marker = f'###CHECK_{compiler_upper}###'
        check_command = f'where {compiler} >nul 2>&1'
        batch_script.extend([
            f'echo {check_marker}',
            f'{check_command}',
            'if %ERRORLEVEL% EQU 0 (',
            f'  echo {available_marker}',
            f'  {info["version_command"]}',
            ') else (',
            f'  echo {not_available_marker}',
            ')'
        ])

    batch_script.append('echo ###END_COMPILER_CHECK###')

    return _execute_check_script(batch_script, compiler_info)


def available_unix_compilers(compiler_info: Dict[str, Dict[str, Any]]):
    shell_script = [
        "#!/bin/bash",
        'echo "###BEGIN_COMPILER_CHECK###"'
    ]

    for compiler, info in compiler_info.items():
        compiler_upper = compiler.upper()
        available_marker = f'{compiler_upper}_AVAILABLE'
        not_available_marker = f'{compiler_upper}_NOT_AVAILABLE'
        check_marker = f'###CHECK_{compiler_upper}###'
        check_command = f'command -v {compiler} >/dev/null 2>&1'
        shell_script.extend([
            f'echo "{check_marker}"',
            f'if {check_command}; then',
            f'  echo "{available_marker}"',
            f'  {info["version_command"]}',
            'else',
            f'  echo "{not_available_marker}"',
            'fi'
        ])

    shell_script.append('echo "###END_COMPILER_CHECK###"')

    return _execute_check_script(shell_script, compiler_info)


def _execute_check_script(script_lines: List[str], compiler_info: Dict):
    windows = Env.platform.windows
    suffix = '.bat' if windows else '.sh'
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w') as script_file:
        script_path = script_file.name
        for line in script_lines:
            script_file.write(f"{line}\n")

    if not windows:
        os.chmod(script_path, 0o755)

    try:
        result = subprocess.run(script_path,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                errors='replace')

        compilers = {}
        output = result.stdout + result.stderr
        start_marker = "###BEGIN_COMPILER_CHECK###"
        end_marker = "###END_COMPILER_CHECK###"

        if start_marker in output and end_marker in output:
            compiler_section = output.split(start_marker)[1].split(end_marker)[0].strip()
            vcvarsall_found = windows and "###VCVARSALL_FOUND###" in output

            make_check_marker = lambda comp: f'###CHECK_{compiler.upper()}###'
            for compiler, info in compiler_info.items():
                if windows and not vcvarsall_found and info.get('requires_vcvarsall', False):
                    continue
                compiler_upper = compiler.upper()
                check_marker = make_check_marker(compiler)
                available_marker = f'{compiler_upper}_AVAILABLE'

                if check_marker in compiler_section:
                    compiler_output = compiler_section.split(check_marker)[1]

                    next_markers = [make_check_marker(other_compiler) for other_compiler, other_info in
                                    compiler_info.items()
                                    if make_check_marker(other_compiler) != check_marker]

                    for marker in next_markers:
                        if marker in compiler_output:
                            compiler_output = compiler_output.split(marker)[0]

                    if available_marker in compiler_output:
                        version_output = compiler_output.split(available_marker)[1].strip()
                        parse_callback = info.get('version_parse_callback', _parse_standard_version_output)
                        version_str = parse_callback(version_output)

                        if version_str:
                            compilers[compiler] = version_str

        return compilers
    except Exception as e:
        system_type = "Windows" if windows else "Unix"
        print(f"Error checking {system_type} compilers: {str(e)}", file=sys.stderr)
        return {}
    finally:
        try:
            os.unlink(script_path)
        except:
            return {}


def _parse_standard_version_output(output: str) -> str:
    lines = []
    for line in output.split("\n"):
        if line.strip() and not line.startswith("###"):
            lines.append(line)
        elif line.startswith("###"):
            break
    return "\n".join(lines).strip()
