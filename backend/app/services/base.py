
from __future__ import annotations

from app.core.config import settings
from app.core.logging import get_logger


class BaseService:
    """
    Parent class for every service.
    """

    def __init__(self) -> None:
        self.settings = settings
        self.logger = get_logger(
            self.__class__.__name__
        )

    def log_start(
        self,
        operation: str,
    ) -> None:
        self.logger.info(
            "Starting %s",
            operation,
        )

    def log_success(
        self,
        operation: str,
    ) -> None:
        self.logger.info(
            "%s completed successfully",
            operation,
        )

    def log_failure(
        self,
        operation: str,
        exc: Exception,
    ) -> None:
        self.logger.exception(
            "%s failed: %s",
            operation,
            exc,
        )