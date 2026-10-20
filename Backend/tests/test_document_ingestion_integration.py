from pathlib import Path

from Backend.app.Services.ingestion.ingestion_service import IngestionService


def test_document_ingestion_integration():
    """
    Tests the connection between a stored document
    and the IngestionService.

    This test does not modify DocumentService.

    If ingestion fails during processing, the test prints
    analysis and routing information so we can identify
    the page and processing strategy that caused the failure.
    """

    file_path = Path(
        "storage/documents/4/"
        "37fc4e03-2ffe-476b-b7a0-d2f19364f455/"
        "CV(UPDATED).pdf"
    )

    document_id = (
        "37fc4e03-2ffe-476b-b7a0-d2f19364f455"
    )

    # ---------------------------------------------------------
    # 1. Verify test document exists
    # ---------------------------------------------------------

    assert file_path.exists(), (
        f"Test document does not exist: {file_path}"
    )

    assert file_path.is_file(), (
        f"Test document path is not a file: {file_path}"
    )

    # ---------------------------------------------------------
    # 2. Create ingestion service
    # ---------------------------------------------------------

    ingestion_service = IngestionService()

    # ---------------------------------------------------------
    # 3. Run ingestion
    # ---------------------------------------------------------

    try:
        result = ingestion_service.process(
            file_path=str(file_path),
            document_id=document_id,
        )

    except ValueError as exc:

        print(
            "\n========== INGESTION FAILURE DEBUG =========="
        )

        print(
            "Error:",
            exc
        )

        # -----------------------------------------------------
        # Re-run the earlier pipeline stages manually.
        #
        # This helps us identify which page and which
        # processing strategy caused the failure.
        # -----------------------------------------------------

        pages = ingestion_service.document_router.parse(
            str(file_path)
        )

        processed_pages = []

        for page in pages:

            raw_text = page["text"]

            if raw_text and raw_text.strip():
                cleaned_text = (
                    ingestion_service.text_cleaner.clean(
                        raw_text
                    )
                )
            else:
                cleaned_text = ""

            processed_pages.append(
                {
                    **page,
                    "text": cleaned_text,
                }
            )

        # -----------------------------------------------------
        # Content analysis
        # -----------------------------------------------------

        analysis = (
            ingestion_service.content_analyzer.analyze(
                processed_pages
            )
        )

        # -----------------------------------------------------
        # Content routing
        # -----------------------------------------------------

        routing = (
            ingestion_service.content_router.route(
                analysis
            )
        )

        # -----------------------------------------------------
        # Print analysis
        # -----------------------------------------------------

        print(
            "\n---------- ANALYSIS ----------"
        )

        for page in analysis["pages"]:

            print(
                "Page:",
                page["page_number"],
                "| Content type:",
                page["content_type"],
                "| Text length:",
                page["text_length"],
                "| Has image:",
                page["has_image"],
                "| OCR recommended:",
                page["ocr_recommended"],
            )

        # -----------------------------------------------------
        # Print routing
        # -----------------------------------------------------

        print(
            "\n---------- ROUTING ----------"
        )

        for page in routing["pages"]:

            print(
                "Page:",
                page["page_number"],
                "| Content type:",
                page["content_type"],
                "| Strategy:",
                page["processing_strategy"],
            )

        print(
            "\nIntegration test stopped for debugging."
        )

        # Re-raise the original exception so the terminal
        # still shows the complete traceback.

        raise

    # ---------------------------------------------------------
    # 4. Successful ingestion assertions
    # ---------------------------------------------------------

    print(
        "\n========== INGESTION INTEGRATION TEST =========="
    )

    print(
        "Document ID:",
        result["document_id"]
    )

    print(
        "Total pages:",
        len(result["pages"])
    )

    print(
        "Pages with text:",
        result["analysis"]["pages_with_text"]
    )

    print(
        "Pages requiring OCR:",
        result["analysis"]["pages_requiring_ocr"]
    )

    print(
        "Routing:",
        result["routing"]["pages"]
    )

    print(
        "Canonical documents:",
        len(result["canonical_documents"])
    )

    # ---------------------------------------------------------
    # 5. Validate document ID
    # ---------------------------------------------------------

    assert result["document_id"] == document_id

    # ---------------------------------------------------------
    # 6. Validate pages
    # ---------------------------------------------------------

    assert len(result["pages"]) > 0

    assert result["analysis"]["total_pages"] > 0

    # ---------------------------------------------------------
    # 7. Validate routing
    # ---------------------------------------------------------

    assert len(result["routing"]["pages"]) == len(
        result["pages"]
    )

    # ---------------------------------------------------------
    # 8. Validate canonical documents
    # ---------------------------------------------------------

    assert len(result["canonical_documents"]) == len(
        result["pages"]
    )

    for canonical_document in result["canonical_documents"]:

        assert (
            canonical_document.document_id
            == document_id
        )

        assert (
            canonical_document.page_number >= 1
        )

    print(
        "\nDocument → Ingestion integration test passed."
    )


if __name__ == "__main__":
    test_document_ingestion_integration()
