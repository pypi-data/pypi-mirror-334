import sys
import argparse
import subprocess
import os


def launch_studio(project_dir):
    from iprm.util.env import Env
    from iprm import studio

    # TODO: Ditch the Rust IPRM Studio Rewrite, only after we have gotten the existing C++ version to the same
    #  level as Rust's dependency graph rendering, as now there is proof that it IS possible to have graphviz-quality
    #  renders from a custom canvas, so it MUST be possible in QTs world as well
    studio_exe_path = os.path.join(os.path.dirname(studio.__file__), 'bin', 'studio')
    args = [studio_exe_path]
    if project_dir:
        args.append(project_dir)
    try:
        if Env.platform.windows:
            subprocess.Popen(
                args, creationflags=subprocess.DETACHED_PROCESS, start_new_session=True
            )
        else:
            subprocess.Popen(
                args, start_new_session=True
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

    args = parser.parse_args()
    sys.exit(launch_studio(args.project_dir))
