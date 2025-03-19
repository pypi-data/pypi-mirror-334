import argparse
import sys
from iprm.load.native import NativeLoader
from iprm.gen.cmake import CMakeGenerator
from iprm.gen.meson import MesonGenerator
from iprm.core.session import Session

BACKENDS = {
    CMakeGenerator.name: CMakeGenerator,
    MesonGenerator.name: MesonGenerator,
    # TODO: For Graphviz, it will only support the `generate` (create a dotfile) and the `build`
    #  (convert dot file into whatever `dot -T` supports)
    # TODO: Add support for Graphviz, Ninja, SCons, and MSBuild
}

GENERATE_CMD = 'generate'
CONFIGURE_CMD = 'configure'
BUILD_CMD = 'build'
TEST_CMD = 'test'
INSTALL_CMD = 'install'


def _generate_main(**kwargs):
    # TODO: Support loading a custom backend from the passed in plugin path
    generator_class = BACKENDS[kwargs.pop('backend')]
    project_dir = kwargs.pop('projdir')
    Session.create(project_dir)
    import platform
    loader = NativeLoader(project_dir, platform.system())
    generator = generator_class(loader, **kwargs)
    generator.generate_project()
    Session.destroy()


def _configure_main(**kwargs):
    generator_class = BACKENDS[kwargs.pop('backend')]
    sys.exit(generator_class.configure(**kwargs))


def _build_main(**kwargs):
    generator_class = BACKENDS[kwargs.pop('backend')]
    sys.exit(generator_class.build(**kwargs))


def _test_main(**kwargs):
    generator_class = BACKENDS[kwargs.pop('backend')]
    sys.exit(generator_class.test(**kwargs))


def _install_main(**kwargs):
    generator_class = BACKENDS[kwargs.pop('backend')]
    sys.exit(generator_class.install(**kwargs))


def _validate_backend(value):
    # TODO: When plugin support is added, don't just validate the main list
    if value.lower() not in BACKENDS:
        raise argparse.ArgumentTypeError(
            f"'{value}' is not supported. Use one of: {', '.join(BACKENDS)}"
        )
    return value.lower()


def main(known_backend=None):
    parser = argparse.ArgumentParser(description='IPRM Command Line Interface')
    parser.add_argument(
        'backend',
        type=_validate_backend,
        help=argparse.SUPPRESS if not known_backend else 'Backend to use'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    backend_help_text = "the specified backend" if not known_backend else known_backend

    generate_parser = subparsers.add_parser('generate', help=f'Generate project files for {backend_help_text}')
    generate_parser.add_argument(
        '--projdir',
        help='Root directory of the IPRM project'
    )

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        '--bindir',
        help='Root binary directory for the project'
    )
    common_parser.add_argument(
        '--buildtype',
        help='Build configuration for the project'
    )

    configure_parser = subparsers.add_parser('configure',
                                             help=f'Configure the generated project files for {backend_help_text}',
                                             parents=[common_parser])
    configure_parser.add_argument(
        '--generator',
        required=False,
        help='Build System to configure (Only required when generator is a project model)'
    )
    configure_parser.add_argument(
        '--srcdir',
        required=False,
        help='Root source directory for the project'
    )

    build_parser = subparsers.add_parser('build',
                                         help=f'Build the generated project files for {backend_help_text}',
                                         parents=[common_parser])
    build_parser.add_argument(
        '--target',
        required=False,
        help='Target to build'
    )
    build_parser.add_argument(
        '--numproc',
        required=False,
        help='Number of available processors on your system to use in build'
    )

    test_parser = subparsers.add_parser('test',
                                        help=f'Test the generated project for {backend_help_text}',
                                        parents=[common_parser])

    # TODO: implement install command

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    kwargs = vars(args)
    backend = kwargs.pop('backend')
    command = kwargs.pop('command')
    if command == GENERATE_CMD:
        # TODO: Support extra utility args (e.g. enable/disable generation cache, etc)
        _generate_main(backend=backend, **kwargs)
    elif command == CONFIGURE_CMD:
        _configure_main(backend=backend, **kwargs)
    elif command == BUILD_CMD:
        _build_main(backend=backend, **kwargs)
    elif command == TEST_CMD:
        _test_main(backend=backend, **kwargs)
    elif command == INSTALL_CMD:
        _install_main(backend=backend, **kwargs)


def _backend_main(backend):
    if len(sys.argv) < 3:
        main(backend)
    else:
        command = sys.argv[1]
        args = sys.argv[2:]
        backend_argv = [
            sys.argv[0],
            backend,
            command,
        ]
        backend_argv.extend(args)
        sys.argv = backend_argv
        main(backend)


def cmake_main():
    _backend_main(CMakeGenerator.name)


def meson_main():
    _backend_main(MesonGenerator.name)


if __name__ == '__main__':
    main()
