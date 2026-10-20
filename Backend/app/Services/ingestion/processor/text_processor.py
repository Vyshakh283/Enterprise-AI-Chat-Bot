from typing import Any

from Backend.app.Services.ingestion.processor.base_processor import (
    BaseProcessor,
)

from Backend.app.Services.ingestion.processor.processor_result import (
    ProcessorResult,
)


class TextProcessor(BaseProcessor):
    """
    Processes content that already contains machine-readable text.
    """

    def process(
        self,
        content: Any,
    ) -> ProcessorResult:

        if not isinstance(content, str):
            raise TypeError(
                "TextProcessor expects content to be a string."
            )

        cleaned_content = content.strip()

        if not cleaned_content:
            raise ValueError(
                "TextProcessor cannot process empty text."
            )

        return ProcessorResult(
            status="success",
            processor="text",
            content_type="text",
            text=cleaned_content,
            structured_data={},
            metadata={},
            confidence=None,
            warnings=[],
            errors=[],
        )