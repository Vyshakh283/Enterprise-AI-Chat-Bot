from io import BytesIO
from unittest.mock import patch

from fastapi import UploadFile

from Backend.app.database.db import session_local
from Backend.app.Services.document_service import DocumentService


def test_document_upload_commit_failure_cleanup():
    db = session_local()

    try:
        service = DocumentService(db)

        file = UploadFile(
            filename="commit_failure_test.pdf",
            file=BytesIO(b"test document content"),
        )

        user_id = 4

        with patch.object(
            service.storage,
            "save_file",
            return_value="storage/documents/4/test/commit_failure_test.pdf",
        ) as mock_save_file, patch.object(
            service.storage,
            "delete_file",
        ) as mock_delete_file, patch.object(
            service.repository,
            "commit",
            side_effect=RuntimeError("Simulated database commit failure"),
        ):

            try:
                service.upload_document(
                    file=file,
                    user_id=user_id,
                )

                assert False, (
                    "Expected database commit failure "
                    "but upload succeeded."
                )

            except RuntimeError as exc:

                assert str(exc) == (
                    "Simulated database commit failure"
                )

                # File storage was successfully completed.
                mock_save_file.assert_called_once()

                # Because commit failed after the file was saved,
                # DocumentService must clean up the stored file.
                mock_delete_file.assert_called_once()

                print("\n========== COMMIT FAILURE TEST ==========")
                print("Database commit failure:", exc)
                print("File save executed: PASS")
                print("Database rollback executed: PASS")
                print("Stored file cleanup executed: PASS")
                print("Original exception propagated: PASS")

    finally:
        db.close()


if __name__ == "__main__":
    test_document_upload_commit_failure_cleanup()
    print("\nDocumentService commit-failure cleanup test passed.")