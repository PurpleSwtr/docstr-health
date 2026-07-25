import sys

from ..core.config import config
from ..core.logger import logger
from ..core.enums import StatusProject, StatusProjectPrioritized
from ..models.report import ProjectReport


class CiFailureChecker:
    def __init__(self, project_report: ProjectReport) -> None:
        self._project_status = project_report.get_project_status()

    def assertion(self) -> None:
        if config.parameters.get("ci", False):
            current_name = StatusProject(self._project_status).name
            failure_name = StatusProject(config.parameters.get("failure_level")).name

            project_priority = StatusProjectPrioritized[current_name].value
            failure_priority = StatusProjectPrioritized[failure_name].value

            logger.debug(f"{project_priority=}, {failure_priority=}")

            if project_priority <= failure_priority:
                sys.exit(1)
