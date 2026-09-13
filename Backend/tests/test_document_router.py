from Backend.app.Services.ingestion.document_router import DocumentRouter


router = DocumentRouter()


pdf_path = (
    "storage/documents/4/"
    "ccca9aad-3217-4c1c-b466-c0b4f6303577/"
    "t1.pdf"
)

txt_path = (
    "storage/test_documents/"
    "test_text.txt"
)

docx_path = (
    "storage/test_documents/"
    "test_document.docx"
)


def test_document(
    label: str,
    file_path: str,
) -> None:

    print(f"\n========== {label} ==========")

    pages = router.parse(file_path)

    print(f"Total routed pages: {len(pages)}")

    for page in pages:
        print(
            f"\n--- PAGE {page['page_number']} ---"
        )
        print(
            f"Text length: {len(page['text'])}"
        )
        print(
            f"Text repr: {page['text']!r}"
        )


test_document("PDF TEST", pdf_path)
test_document("TXT TEST", txt_path)
test_document("DOCX TEST", docx_path)