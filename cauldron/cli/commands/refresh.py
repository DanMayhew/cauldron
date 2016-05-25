from argparse import ArgumentParser

import cauldron
from cauldron import environ

DESCRIPTION = """
    Rewrites the current state of the project to the results directory for
    viewing. Useful when you want to update included and dependency files
    without re-running the analysis steps.
    """


def prepare(parser: ArgumentParser):
    pass


def execute(parser: ArgumentParser):
    """

    :return:
    """

    project = cauldron.project
    if project:
        project = project.internal_project

    if not project:
        environ.log(
            '[ABORTED]: No project is open. Unable to refresh.',
            whitespace=1
        )
        return

    project.write()

    environ.log(
        '[COMPLETE]: Project display refreshed',
        whitespace=1
    )


