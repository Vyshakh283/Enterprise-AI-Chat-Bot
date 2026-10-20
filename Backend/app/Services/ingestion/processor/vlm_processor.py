from typing import Any

from Backend.app.Services.ingestion.processor.base_processor import (
    BaseProcessor,
)

from Backend.app.Services.ingestion.processor.processor_result import (
    ProcessorResult,
)


class VLMProcessor(BaseProcessor):
    """
    Processes visual content using a Vision Language Model.
    """

    def process(
        self,
        content: Any,
    ) -> ProcessorResult:

        if content is None:
            raise ValueError(
                "VLMProcessor cannot process None content."
            )

        return ProcessorResult(
            status="not_implemented",
            processor="vlm",
            content_type="visual",
            text=None,
            structured_data={},
            metadata={
                "message": (
                    "VLM provider integration is pending."
                )
            },
            confidence=None,
            warnings=[
                "VLM provider integration is pending."
            ],
            errors=[],
        )