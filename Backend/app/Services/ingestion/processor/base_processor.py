from abc import ABC, abstractmethod
from typing import Any

from Backend.app.Services.ingestion.processor.processor_result import (
    ProcessorResult,
)


class BaseProcessor(ABC):
    """
    Common contract for all document-content processors.

    Every processor must implement the process() method
    and return a ProcessorResult.
    """

    @abstractmethod
    def process(
        self,
        content: Any,
    ) -> ProcessorResult:
        raise NotImplementedError