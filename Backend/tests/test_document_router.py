from Backend.app.Services.ingestion.document_router import DocumentRouter


if __name__ == "__main__":

    router = DocumentRouter()

    file_path = (
        "storage/test_documents/test_text.txt"
    )

    pages = router.parse(file_path)

    print(
        f"\nTotal routed pages: {len(pages)}"
    )

    for page in pages:

        print(
            f"\n========== PAGE "
            f"{page['page_number']} =========="
        )

        print(
            f"Text length: {len(page['text'])}"
        )

        print(
            f"Text repr: {repr(page['text'][:1000])}"
        )