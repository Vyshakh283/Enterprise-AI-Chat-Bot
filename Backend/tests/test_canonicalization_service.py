from Backend.app.Services.ingestion.canonical_document import (
    CanonicalDocument,
)

from Backend.app.Services.ingestion.canonicalization_service import (
    CanonicalizationService,
)

from Backend.app.Services.ingestion.processor.processor_result import (
    ProcessorResult,
)


def test_canonicalization() -> None:

    service = CanonicalizationService()

    processor_result = ProcessorResult(
        status="success",
        processor="text",
        content_type="text",
        text="Enterprise AI Chatbot",
        structured_data={
            "department": "AI/ML"
        },
        metadata={
            "source_format": "pdf"
        },
        confidence=0.99,
    )

    result = service.canonicalize(
        document_id="doc-001",
        page_number=1,
        processor_result=processor_result,
    )

    assert isinstance(
        result,
        CanonicalDocument,
    )

    assert result.document_id == "doc-001"
    assert result.page_number == 1
    assert result.content_type == "text"
    assert result.text == "Enterprise AI Chatbot"

    assert result.structured_data == {
        "department": "AI/ML"
    }

    assert result.metadata == {
        "source_format": "pdf"
    }

    assert result.processor == "text"
    assert result.confidence == 0.99

    print(
        "\n========== CANONICALIZATION SERVICE =========="
    )

    print(result.to_dict())

    print(
        "\nCanonicalization service test passed."
    )


if __name__ == "__main__":
    test_canonicalization()