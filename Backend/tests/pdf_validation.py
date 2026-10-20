from Backend.app.Services.ingestion.pdf_extractor import PDFParser

def test_invalid_file_type() -> None:
    parser = PDFParser()

    try:
        parser.parse(
            "storage/test_documents/test.txt"
        )

    except ValueError as exc:
        print(
            f"PASS: Invalid file type test - {exc}"
        )

    except Exception as exc:
        print(
            "FAIL: Invalid file type test - "
            f"Expected ValueError, "
            f"got {type(exc).__name__}: {exc}"
        )

    else:
        print(
            "FAIL: Invalid file type test - "
            "No exception was raised."
        )
        
def test_missing_file() -> None:
    parser = PDFParser()

    try:
        parser.parse(
            "storage/test_documents/does_not_exist.pdf"
        )

    except FileNotFoundError as exc:
        print(
            f"PASS: Missing file test - {exc}"
        )

    except Exception as exc:
        print(
            "FAIL: Missing file test - "
            f"Expected FileNotFoundError, "
            f"got {type(exc).__name__}: {exc}"
        )

    else:
        print(
            "FAIL: Missing file test - "
            "No exception was raised."
        )



if __name__ == "__main__":
    print(
        "\n========== PDF PARSER ERROR TESTS =========="
    )

    test_missing_file()
    test_invalid_file_type()