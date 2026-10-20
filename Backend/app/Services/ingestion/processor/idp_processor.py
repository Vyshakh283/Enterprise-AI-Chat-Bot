from typing import Any

from Backend.app.Services.ingestion.processor.base_processor import (
    BaseProcessor,
)

from Backend.app.Services.ingestion.processor.processor_result import (
    ProcessorResult,
)


class IDPProcessor(BaseProcessor):
    """
    Processes documents using Intelligent Document Processing.
    """

    def process(
        self,
        content: Any,
    ) -> ProcessorResult:

        if content is None:
            raise ValueError(
                "IDPProcessor cannot process None content."
            )

        return ProcessorResult(
            status="not_implemented",
            processor="idp",
            content_type="structured_document",
            text=None,
            structured_data={},
            metadata={
                "message": (
                    "IDP provider integration is pending."
                )
            },
            confidence=None,
            warnings=[
                "IDP provider integration is pending."
            ],
            errors=[],
        )