import typing

import cauldron
from cauldron import environ
from cauldron.runner import source
from cauldron.session.project import Project
from cauldron.session.project import ProjectStep


def dependencies(
    project: Project,
    force: bool = False
) -> bool:
    """

    :param project:
    :param force:
    :return:
    """

    for pd in project.dependencies:
        if not source.source_dependency(project, pd):
            return False

    return True


def initialize(project: typing.Union[str, Project]):
    """

    :param project:
    :return:
    """

    if isinstance(project, str):
        project = Project(source_directory=project)

    cauldron.project.load(project)
    return project


def section(
        project: typing.Union[Project, None],
        starting: ProjectStep = None,
        limit: int = 1
) -> str:
    """

    :param project:
    :param starting:
    :param limit:
    :return:
    """

    if project is None:
        project = cauldron.project.internal_project

    if not dependencies(project):
        return None

    starting_index = 0
    if starting:
        starting_index = project.steps.index(starting)
    count = 0

    for ps in project.steps:
        if count >= limit:
            break

        if ps.index < starting_index:
            continue

        if count == 0 and not ps.is_dirty():
            continue

        if not source.run_step(project, ps):
            project.write()
            return None

        count += 1

    return project.write()


def complete(
        project: typing.Union[Project, None],
        starting: ProjectStep = None,
        force: bool = False,
        limit: int = -1
) -> str:
    """
    Runs the entire project, writes the results files, and returns the URL to
    the report file

    :param project:
    :param starting:
    :param force:
    :param limit:
    :return:
        Local URL to the report path
    """

    if project is None:
        project = cauldron.project.internal_project

    if not dependencies(project):
        return None

    starting_index = 0
    if starting:
        starting_index = project.steps.index(starting)
    count = 0

    for ps in project.steps:
        if 0 < limit <= count:
            break

        if ps.index < starting_index:
            continue

        if not force and not ps.is_dirty():
            if limit < 1:
                environ.log('[{}]: Nothing to update'.format(ps.id))
            continue

        count += 1

        if not source.run_step(project, ps, force=True):
            project.write()
            return None

    return project.write()

