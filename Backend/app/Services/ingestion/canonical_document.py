from typing import Any


class CanonicalDocument:
    """
    Standard internal representation of processed document content.

    All processors should eventually produce data that can be
    converted into this structure.
    """

    def __init__(
        self,
        document_id: str,
        page_number: int,
        content_type: str,
        text: str | None = None,
        structured_data: dict[str, Any] | None = None,
        visual_description: str | None = None,
        metadata: dict[str, Any] | None = None,
        processor: str | None = None,
        confidence: float | None = None,
    ) -> None:

        if not document_id.strip():
            raise ValueError(
                "document_id cannot be empty."
            )

        if page_number < 1:
            raise ValueError(
                "page_number must be greater than zero."
            )

        if not content_type.strip():
            raise ValueError(
                "content_type cannot be empty."
            )

        if confidence is not None:
            if not 0.0 <= confidence <= 1.0:
                raise ValueError(
                    "confidence must be between 0.0 and 1.0."
                )

        self.document_id = document_id
        self.page_number = page_number
        self.content_type = content_type
        self.text = text
        self.structured_data = (
            structured_data
            if structured_data is not None
            else {}
        )
        self.visual_description = visual_description
        self.metadata = (
            metadata
            if metadata is not None
            else {}
        )
        self.processor = processor
        self.confidence = confidence

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the canonical document into a dictionary.
        """

        return {
            "document_id": self.document_id,
            "page_number": self.page_number,
            "content_type": self.content_type,
            "text": self.text,
            "structured_data": self.structured_data,
            "visual_description": self.visual_description,
            "metadata": self.metadata,
            "processor": self.processor,
            "confidence": self.confidence,
        }