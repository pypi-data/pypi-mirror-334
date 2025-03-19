import argparse
import sys

from iprm.cli.app import main as cli_main
from iprm.cli.app import cmake_main as cli_cmake_main
from iprm.cli.app import meson_main as cli_meson_main
from iprm.studio_cxx.app import main as studio_cxx_main
from iprm.studio_rust.app import main as studio_rust_main


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--cli', action='store_true', help='IPRM Command Line Interface')
    parser.add_argument('--studio', action='store_true', help='IPRM Studio')
    args, remaining_args = parser.parse_known_args()
    sys.argv = [sys.argv[0]] + remaining_args
    if args.cli:
        cli_main()
    elif args.studio:
        studio_cxx_main()


if __name__ == '__main__':
    main()
