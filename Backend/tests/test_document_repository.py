from Backend.app.Models.user import User
from Backend.app.Models.conversation import Conversation
from Backend.app.Models.Document import Document
from Backend.app.Models.Document_chunks import document_chunks
from Backend.app.Models.Embedding_model import Embedding
from Backend.app.Models.AuditLog import AuditLog

from Backend.app.database.db import session_local
from Backend.app.repositories.document_repository import DocumentRepository


def test_get_document_by_id():

    db = session_local()

    try:

        repository = DocumentRepository(db)

        document = repository.get_by_id(9)

        assert document is not None

        print("\n========== DOCUMENT BY ID ==========")
        print("ID:", document.id)
        print("UUID:", document.document_uuid)
        print("Filename:", document.filename)
        print("User ID:", document.user_id)
        print("Status:", document.processing_status)

    finally:

        db.close()


def test_get_documents_by_user_id():

    db = session_local()

    try:

        repository = DocumentRepository(db)

        documents = repository.get_by_user_id(4)

        print("\n========== DOCUMENTS BY USER ==========")
        print("Total documents:", len(documents))

        for document in documents:

            print(
                "ID:",
                document.id,
                "| Filename:",
                document.filename,
                "| Status:",
                document.processing_status,
            )

        assert len(documents) > 0

    finally:

        db.close()


if __name__ == "__main__":

    test_get_document_by_id()

    test_get_documents_by_user_id()

    print("\nDocument repository retrieval tests passed.")