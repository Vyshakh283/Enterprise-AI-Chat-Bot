from typing import Any


class ProcessorResult:
    """
    Standard result produced by every document processor.

    This creates a common contract between processors
    and the downstream canonicalization layer.
    """

    VALID_STATUSES = {
        "success",
        "not_implemented",
        "failed",
    }

    def __init__(
        self,
        status: str,
        processor: str,
        content_type: str,
        text: str | None = None,
        structured_data: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        confidence: float | None = None,
        warnings: list[str] | None = None,
        errors: list[str] | None = None,
    ) -> None:

        if status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid processor status: {status}"
            )

        if not processor.strip():
            raise ValueError(
                "processor cannot be empty."
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

        self.status = status
        self.processor = processor
        self.content_type = content_type
        self.text = text

        self.structured_data = (
            structured_data
            if structured_data is not None
            else {}
        )

        self.metadata = (
            metadata
            if metadata is not None
            else {}
        )

        self.confidence = confidence

        self.warnings = (
            warnings
            if warnings is not None
            else []
        )

        self.errors = (
            errors
            if errors is not None
            else []
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert processor result into a dictionary.
        """

        return {
            "status": self.status,
            "processor": self.processor,
            "content_type": self.content_type,
            "text": self.text,
            "structured_data": self.structured_data,
            "metadata": self.metadata,
            "confidence": self.confidence,
            "warnings": self.warnings,
            "errors": self.errors,
        }