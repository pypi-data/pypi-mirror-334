"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
import sys
import argparse
import subprocess
import os


def launch_studio():
    from iprm import studio
    from iprm.util.env import Env
    studio_exe_name = f'studio{".exe" if Env.platform.windows else ""}'
    studio_exe_path = os.path.join(os.path.dirname(studio.__file__), 'bin', studio_exe_name)
    try:
        if Env.platform.windows:
            subprocess.Popen(
                [studio_exe_path, *sys.argv[1:]],
                creationflags=subprocess.DETACHED_PROCESS,
                start_new_session=True
            )
        else:
            subprocess.Popen(
                [studio_exe_path, *sys.argv[1:]],
                start_new_session=True
            )
        return 0

    except Exception as e:
        print(f"Unable to launch IPRM Studio: {e}", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(description="IPRM Studio")
    parser.add_argument(
        "project_dir",
        type=str,
        nargs='?',
        help="Path to the project directory"
    )

    parser.parse_args()
    sys.exit(launch_studio())
