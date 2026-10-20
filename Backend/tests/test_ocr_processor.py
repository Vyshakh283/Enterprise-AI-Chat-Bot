
from pathlib import Path

from Backend.app.Services.ingestion.processor.ocr_processor import (
    OCRProcessor,
)


def main() -> None:
    pdf_path = Path(
        "storage/documents/4/37fc4e03-2ffe-476b-b7a0-d2f19364f455/"
        "CV(UPDATED).pdf"
    )

    if not pdf_path.is_file():
        raise FileNotFoundError(
            f"Test PDF not found: {pdf_path}"
        )

    processor = OCRProcessor(
        language="en",
        device="cpu",
    )

    result = processor.process(
        {
            "file_path": pdf_path,
            "page_number": 1,
        }
    )

    print("Status:", result.status)
    print("Processor:", result.processor)
    print("Confidence:", result.confidence)
    print("Metadata:", result.metadata)
    print("Warnings:", result.warnings)
    print("Errors:", result.errors)
    print("\nExtracted text:\n", result.text)

    assert result.status == "success", result.errors
    assert result.text, "OCR returned no text."
    assert "VYSHAKH" in result.text.upper(), (
        "Expected name was not found in OCR output."
    )


if __name__ == "__main__":
    main()
