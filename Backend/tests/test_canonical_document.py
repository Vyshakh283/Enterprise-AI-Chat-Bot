from Backend.app.Services.ingestion.canonical_document import (
    CanonicalDocument,
)


def test_canonical_document() -> None:
    document = CanonicalDocument(
        document_id="doc-001",
        page_number=1,
        content_type="text",
        text="Enterprise AI Chatbot",
        structured_data={
            "department": "AI/ML"
        },
        metadata={
            "source_format": "pdf"
        },
        processor="text",
        confidence=0.99,
    )

    result = document.to_dict()

    assert result["document_id"] == "doc-001"
    assert result["page_number"] == 1
    assert result["content_type"] == "text"
    assert result["text"] == "Enterprise AI Chatbot"
    assert result["structured_data"]["department"] == "AI/ML"
    assert result["processor"] == "text"
    assert result["confidence"] == 0.99

    print(
        "========== CANONICAL DOCUMENT TEST =========="
    )
    print(result)


if __name__ == "__main__":
    test_canonical_document()
    print("Canonical document test passed.")