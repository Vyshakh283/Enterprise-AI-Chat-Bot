from typing import Any

from Backend.app.Services.ingestion.processor.base_processor import (
    BaseProcessor,
)

from Backend.app.Services.ingestion.processor.processor_result import (
    ProcessorResult,
)


class EmptyContentProcessor(BaseProcessor):
    """
    Handles pages where no usable content was extracted.

    This processor does not treat the page as a failure.
    The page may simply be intentionally blank.
    """

    def process(
        self,
        content: Any,
    ) -> ProcessorResult:

        return ProcessorResult(
            status="success",
            processor="empty",
            content_type="empty",
            text=None,
            structured_data={},
            metadata={
                "message": (
                    "No usable content was extracted from the page."
                )
            },
            confidence=None,
            warnings=[
                "No usable content was extracted."
            ],
            errors=[],
        )