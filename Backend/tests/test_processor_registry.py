from Backend.app.Services.ingestion.processor import (
    EmptyContentProcessor,
    IDPProcessor,
    MixedContentProcessor,
    OCRProcessor,
    ProcessorRegistry,
    TextProcessor,
    VLMProcessor,
)


def test_processor_registry() -> None:

    registry = ProcessorRegistry()

    text_processor = registry.get(
        "text_processing"
    )

    ocr_processor = registry.get(
        "ocr"
    )

    idp_processor = registry.get(
        "idp"
    )

    vlm_processor = registry.get(
        "vlm"
    )

    mixed_processor = registry.get(
        "mixed_content_processing"
    )

    empty_processor = registry.get(
        "empty_content"
    )

    assert isinstance(
        text_processor,
        TextProcessor,
    )

    assert isinstance(
        ocr_processor,
        OCRProcessor,
    )

    assert isinstance(
        idp_processor,
        IDPProcessor,
    )

    assert isinstance(
        vlm_processor,
        VLMProcessor,
    )

    assert isinstance(
        mixed_processor,
        MixedContentProcessor,
    )

    assert isinstance(
        empty_processor,
        EmptyContentProcessor,
    )

    print(
        "\n========== PROCESSOR REGISTRY =========="
    )

    print(
        "text_processing → "
        f"{type(text_processor).__name__}"
    )

    print(
        "ocr → "
        f"{type(ocr_processor).__name__}"
    )

    print(
        "idp → "
        f"{type(idp_processor).__name__}"
    )

    print(
        "vlm → "
        f"{type(vlm_processor).__name__}"
    )

    print(
        "mixed_content_processing → "
        f"{type(mixed_processor).__name__}"
    )

    print(
        "empty_content → "
        f"{type(empty_processor).__name__}"
    )

    print(
        "\nProcessor registry test passed."
    )


if __name__ == "__main__":
    test_processor_registry()
    