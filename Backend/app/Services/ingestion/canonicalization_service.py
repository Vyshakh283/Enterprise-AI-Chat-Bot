from Backend.app.Services.ingestion.canonical_document import (
    CanonicalDocument,
)

from Backend.app.Services.ingestion.processor.processor_result import (
    ProcessorResult,
)


class CanonicalizationService:
    """
    Converts ProcessorResult objects into CanonicalDocument objects.

    Responsibilities:
    - Validate processor output
    - Apply document and page identity
    - Convert standardized processor results
      into the canonical internal representation

    This service does not:
    - Parse files
    - Perform OCR
    - Call IDP providers
    - Call VLM providers
    - Generate embeddings
    """

    def canonicalize(
        self,
        document_id: str,
        page_number: int,
        processor_result: ProcessorResult,
    ) -> CanonicalDocument:
        """
        Convert one ProcessorResult into a CanonicalDocument.
        """

        # Validate document identity
        if not isinstance(document_id, str):
            raise TypeError(
                "document_id must be a string."
            )

        if not document_id.strip():
            raise ValueError(
                "document_id cannot be empty."
            )

        # Validate page identity
        if not isinstance(page_number, int):
            raise TypeError(
                "page_number must be an integer."
            )

        if page_number < 1:
            raise ValueError(
                "page_number must be greater than zero."
            )

        # Validate processor result
        if not isinstance(
            processor_result,
            ProcessorResult,
        ):
            raise TypeError(
                "processor_result must be a ProcessorResult."
            )

        # Only successful processing can be canonicalized
        if processor_result.status != "success":
            raise ValueError(
                "Cannot canonicalize unsuccessful "
                "processor result."
            )

        return CanonicalDocument(
            document_id=document_id,
            page_number=page_number,
            content_type=processor_result.content_type,
            text=processor_result.text,
            structured_data=processor_result.structured_data,
            metadata=processor_result.metadata,
            processor=processor_result.processor,
            confidence=processor_result.confidence,
        )