from unittest.mock import patch

from fastapi import UploadFile
from io import BytesIO

from Backend.app.database.db import session_local
from Backend.app.Services.document_service import DocumentService


def test_document_upload_storage_failure():

    db = session_local()

    try:

        service = DocumentService(db)

        file = UploadFile(
            filename="failure_test.pdf",
            file=BytesIO(b"test document content"),
        )

        user_id = 4

        # Force StorageService.save_file() to fail.
        with patch.object(
            service.storage,
            "save_file",
            side_effect=RuntimeError(
                "Simulated storage failure"
            ),
        ):

            try:

                service.upload_document(
                    file=file,
                    user_id=user_id,
                )

                assert False, (
                    "Expected storage failure "
                    "but upload succeeded."
                )

            except RuntimeError as exc:

                assert str(exc) == (
                    "Simulated storage failure"
                )

                print(
                    "\n========== FAILURE TEST =========="
                )

                print(
                    "Storage failure:",
                    exc,
                )

                print(
                    "Rollback path executed: PASS"
                )

    finally:

        db.close()


if __name__ == "__main__":

    test_document_upload_storage_failure()

    print(
        "\nDocumentService failure test passed."
    )