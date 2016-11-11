#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser

MY_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


def run():
    try:
        import cauldron
    except ImportError:
        sys.path.append(os.path.abspath(os.path.join(MY_DIRECTORY, '..', '..')))

        try:
            import cauldron
        except ImportError:
            raise ImportError(' '.join((
                'Unable to import cauldron.'
                'The package was not installed in a known location.'
            )))

    from cauldron.cli.shell import CauldronShell
    from cauldron import environ
    from cauldron.cli import batcher


    parser = ArgumentParser(
        description='Cauldron'
    )

    parser.add_argument(
        '-v', '--version',
        dest='version',
        default=False,
        action='store_true'
    )

    parser.add_argument(
        '-p', '--project',
        dest='project_directory',
        type=str,
        default=None
    )

    parser.add_argument(
        '-l', '--log',
        dest='logging_path',
        type=str,
        default=None
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_directory',
        type=str,
        default=None
    )

    args = parser.parse_args()

    if args.version:
        print('VERSION: {}'.format(environ.package_settings().get('version', 'unknown')))
        sys.exit(0)

    if args.project_directory:
        batcher.run_project(
            project_directory=args.project_directory,
            log_path=args.logging_path,
            output_directory=args.output_directory
        )
        sys.exit(0)

    CauldronShell().cmdloop()