import logging
from pathlib import Path
from uuid import uuid4

from Backend.app.Models.Document import Document
from Backend.app.Models.Enum import Document_Status
from Backend.app.Services.storage_service import StorageService
from Backend.app.repositories.document_repository import (
    DocumentRepository,
)


logger = logging.getLogger(__name__)


class DocumentService:

    def __init__(self, db):

        self.repository = DocumentRepository(db)

        self.storage = StorageService()

    def upload_document(
        self,
        file,
        user_id: int,
    ) -> Document:

        # ==================================================
        # 1. VALIDATE FILENAME
        # ==================================================


        if not file.filename:

            raise ValueError(
                "Uploaded file must have a filename"
            )

        # Remove any client supplied path.
        original_filename = Path(
            file.filename
        ).name

        if not original_filename:

            raise ValueError(
                "Invalid filename"
            )

        # ==================================================
        # 2. FILE EXTENSION
        # ==================================================

        file_extension = ""
   
        if "." in original_filename:

            file_extension = (
                original_filename
                .rsplit(".", 1)[1]
                .lower()
            )

        # ==================================================
        # 3. FILE SIZE
        # ==================================================

        file.file.seek(0, 2)

        file_size = file.file.tell()

        file.file.seek(0)

        # ==================================================
        # 4. GENERATE UNIQUE DOCUMENT ID
        # ==================================================

        document_uuid = uuid4()

        # ==================================================
        # 5. GENERATE FINAL STORAGE KEY
        # ==================================================

        storage_key = (
            f"{user_id}/"
            f"{document_uuid}/"
            f"{original_filename}"
        )

        logger.info(
            "Starting document upload | "
            "user_id=%s | "
            "document_uuid=%s | "
            "filename=%s",
            user_id,
            document_uuid,
            original_filename,
        )

        # Tracks whether physical storage
        # was successfully created.
        file_saved = False

        try:

            # ==================================================
            # 6. CREATE DOCUMENT DATABASE OBJECT
            # ==================================================

            document = Document(

                document_uuid=document_uuid,

                filename=original_filename,

                original_filename=original_filename,

                file_path=storage_key,

                file_type=file_extension,

                mime_type=(
                    file.content_type
                    or "application/octet-stream"
                ),

                file_size=file_size,

                processing_status=(
                    Document_Status.UPLOADED
                ),

                user_id=user_id,
            )

            # ==================================================
            # 7. INSERT INTO POSTGRESQL
            # ==================================================

            self.repository.create(
                document
            )

            logger.info(
                "Document database record "
                "created | "
                "document_id=%s | "
                "document_uuid=%s",
                document.id,
                document_uuid,
            )

            # ==================================================
            # 8. SAVE ORIGINAL FILE
            # ==================================================

            self.storage.save_file(

                file=file,

                storage_key=storage_key,
            )

            file_saved = True

            logger.info(
                "Document file stored | "
                "document_id=%s | "
                "storage_key=%s",
                document.id,
                storage_key,
            )

            # ==================================================
            # 9. COMMIT DATABASE TRANSACTION
            # ==================================================

            self.repository.commit()

            logger.info(
                "Document upload completed | "
                "document_id=%s | "
                "document_uuid=%s",
                document.id,
                document_uuid,
            )

            return document

        except Exception:

            # ==================================================
            # 10. LOG ORIGINAL FAILURE
            # ==================================================

            logger.exception(
                "Document upload failed | "
                "user_id=%s | "
                "document_uuid=%s",
                user_id,
                document_uuid,
            )

            # ==================================================
            # 11. DATABASE ROLLBACK
            # ==================================================

            try:

                self.repository.rollback()

                logger.info(
                    "Database transaction rolled back | "
                    "document_uuid=%s",
                    document_uuid,
                )

            except Exception:

                logger.exception(
                    "CRITICAL: Database rollback failed | "
                    "document_uuid=%s",
                    document_uuid,
                )

            # ==================================================
            # 12. FILE CLEANUP
            # ==================================================

            if file_saved:

                try:

                    self.storage.delete_file(
                        storage_key
                    )

                    logger.info(
                        "Stored file cleaned up | "
                        "document_uuid=%s | "
                        "storage_key=%s",
                        document_uuid,
                        storage_key,
                    )

                except Exception:

                    # IMPORTANT:
                    # Do not hide the original exception.
                    logger.exception(
                        "CRITICAL: File cleanup failed | "
                        "manual cleanup may be required | "
                        "document_uuid=%s | "
                        "storage_key=%s",
                        document_uuid,
                        storage_key,
                    )

            # ==================================================
            # 13. RE-RAISE ORIGINAL EXCEPTION
            # ==================================================

            raise