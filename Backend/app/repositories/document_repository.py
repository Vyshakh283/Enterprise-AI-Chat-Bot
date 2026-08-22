from sqlalchemy.orm import Session

from Backend.app.Models.Document import Document


class DocumentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        document: Document,
    ) -> Document:

        self.db.add(document)

        # Sends INSERT to PostgreSQL and generates
        # document.id without committing.
        self.db.flush()

        return document

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def get_by_id(
        self,
        document_id: int,
    ) -> Document | None:

        return (
            self.db
            .query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

    def get_by_user_id(
        self,
        user_id: int,
    ) -> list[Document]:

        return (
            self.db
            .query(Document)
            .filter(
                Document.user_id == user_id
            )
            .all()
        )