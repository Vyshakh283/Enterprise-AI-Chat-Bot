from Backend.app.Services.ingestion.processor.processor_result import (
    ProcessorResult,
)


def test_processor_result() -> None:

    result = ProcessorResult(
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
        warnings=[],
        errors=[],
    )

    output = result.to_dict()

    assert output["status"] == "success"
    assert output["processor"] == "text"
    assert output["content_type"] == "text"
    assert output["text"] == "Enterprise AI Chatbot"
    assert output["confidence"] == 0.99
    assert output["warnings"] == []
    assert output["errors"] == []

    print(
        "\n========== PROCESSOR RESULT TEST =========="
    )

    print(output)


if __name__ == "__main__":
    test_processor_result()

    print(
        "\nProcessor result test passed."
    )