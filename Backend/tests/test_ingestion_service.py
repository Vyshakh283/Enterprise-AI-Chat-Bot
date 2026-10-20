from Backend.app.Services.ingestion.ingestion_service import (
    IngestionService,
)


service = IngestionService()


test_files = [
    (
        "TXT",
        "storage/test_documents/test_text.txt",
    ),
    (
        "DOCX",
        "storage/test_documents/test_document.docx",
    ),
    (
        "PDF",
        "storage/documents/4/ccca9aad-3217-4c1c-b466-c0b4f6303577/t1.pdf",
    ),
]


for file_type, file_path in test_files:

    print(
        f"\n\n========== {file_type} TEST =========="
    )

    result = service.process(
        file_path,
        document_id=f"test-{file_type.lower()}-001",
    )

    analysis = result["analysis"]
    routing = result["routing"]

    print(
        f"Total pages: "
        f"{analysis['total_pages']}"
    )

    print(
        f"Pages with text: "
        f"{analysis['pages_with_text']}"
    )

    print(
        f"Pages with images: "
        f"{analysis['pages_with_images']}"
    )

    print(
        f"Pages requiring OCR: "
        f"{analysis['pages_requiring_ocr']}"
    )

    for page, analyzed_page, routed_page in zip(
        result["pages"],
        analysis["pages"],
        routing["pages"],
    ):

        page_number = page["page_number"]

        print(
            f"\n--- PAGE {page_number} ---"
        )

        print(
            f"Content type: "
            f"{analyzed_page['content_type']}"
        )

        print(
            f"Processing strategy: "
            f"{routed_page['processing_strategy']}"
        )

        print(
            f"Text: {page['text']!r}"
        )

    print(
        "\n--- CANONICAL DOCUMENTS ---"
    )

    for canonical_document in result[
        "canonical_documents"
    ]:

        print(
            canonical_document.to_dict()
        )