from typing import Any

from Backend.app.Services.ingestion.processor.base_processor import (
    BaseProcessor,
)

from Backend.app.Services.ingestion.processor.processor_result import (
    ProcessorResult,
)


class MixedContentProcessor(BaseProcessor):
    """
    Processes pages containing both text and visual content.

    The current implementation preserves the extracted text.
    Visual understanding will be added later through OCR/VLM
    processing when required.
    """

    def process(
        self,
        content: Any,
    ) -> ProcessorResult:

        if not isinstance(content, str):
            raise TypeError(
                "MixedContentProcessor expects content to be a string."
            )

        cleaned_content = content.strip()

        if not cleaned_content:
            raise ValueError(
                "MixedContentProcessor requires extracted text."
            )

        return ProcessorResult(
            status="success",
            processor="mixed",
            content_type="mixed",
            text=cleaned_content,
            structured_data={},
            metadata={
                "message": (
                    "Mixed content preserved. "
                    "Visual processing is pending."
                )
            },
            confidence=None,
            warnings=[
                "Visual processing is pending."
            ],
            errors=[],
        )