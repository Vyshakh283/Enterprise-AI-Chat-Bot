from Backend.app.Services.ingestion.processor import (
    IDPProcessor,
    OCRProcessor,
    ProcessorResult,
    TextProcessor,
    VLMProcessor,
)


def test_text_processor() -> None:

    processor = TextProcessor()

    result = processor.process(
        "  Enterprise AI Chatbot Text  "
    )

    assert isinstance(result, ProcessorResult)
    assert result.status == "success"
    assert result.processor == "text"
    assert result.content_type == "text"
    assert result.text == "Enterprise AI Chatbot Text"

    print("\n========== TEXT PROCESSOR ==========")
    print(result.to_dict())


def test_ocr_processor() -> None:

    processor = OCRProcessor()

    result = processor.process(
        "image-content"
    )

    assert isinstance(result, ProcessorResult)
    assert result.status == "not_implemented"
    assert result.processor == "ocr"
    assert result.content_type == "image"

    print("\n========== OCR PROCESSOR ==========")
    print(result.to_dict())


def test_idp_processor() -> None:

    processor = IDPProcessor()

    result = processor.process(
        "structured-document-content"
    )

    assert isinstance(result, ProcessorResult)
    assert result.status == "not_implemented"
    assert result.processor == "idp"
    assert result.content_type == "structured_document"

    print("\n========== IDP PROCESSOR ==========")
    print(result.to_dict())


def test_vlm_processor() -> None:

    processor = VLMProcessor()

    result = processor.process(
        "visual-content"
    )

    assert isinstance(result, ProcessorResult)
    assert result.status == "not_implemented"
    assert result.processor == "vlm"
    assert result.content_type == "visual"

    print("\n========== VLM PROCESSOR ==========")
    print(result.to_dict())


if __name__ == "__main__":

    test_text_processor()
    test_ocr_processor()
    test_idp_processor()
    test_vlm_processor()

    print("\nAll processor tests passed.")