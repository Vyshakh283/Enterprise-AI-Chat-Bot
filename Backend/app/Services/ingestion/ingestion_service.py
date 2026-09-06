from Backend.app.Services.ingestion.document_router import DocumentRouter
from Backend.app.Services.ingestion.text_cleaner import TextCleaner


class IngestionService:
    """
    Coordinates document extraction and text cleaning.

    The service does not know which parser should handle
    a particular document. DocumentRouter handles that decision.
    """

    def __init__(self) -> None:
        self.document_router = DocumentRouter()
        self.text_cleaner = TextCleaner()

    def process(
        self,
        file_path: str,
    ) -> list[dict]:
        """
        Extract and clean a document.

        The DocumentRouter selects the appropriate parser
        based on the file extension.
        """

        pages = self.document_router.parse(
            file_path
        )

        processed_pages: list[dict] = []

        for page in pages:

            cleaned_text = self.text_cleaner.clean(
                page["text"]
            )

            processed_pages.append(
                {
                    "page_number": page["page_number"],
                    "text": cleaned_text,
                }
            )

        return processed_pages