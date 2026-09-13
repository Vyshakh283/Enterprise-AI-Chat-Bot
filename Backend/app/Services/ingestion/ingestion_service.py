from typing import Any

from Backend.app.Services.ingestion.document_router import DocumentRouter
from Backend.app.Services.ingestion.text_cleaner import TextCleaner
from Backend.app.Services.ingestion.content_analyzer import ContentAnalyzer
from Backend.app.Services.ingestion.content_router import ContentRouter


class IngestionService:
    """
    Coordinates document extraction, text cleaning,
    content analysis, and content routing.

    Responsibilities:
    - Route document to the correct parser
    - Extract document content
    - Clean extracted text
    - Analyze page content
    - Determine downstream processing strategy

    This service does NOT:
    - Perform OCR
    - Perform IDP
    - Call VLMs
    - Generate embeddings
    - Store vectors
    """

    def __init__(self) -> None:
        self.document_router = DocumentRouter()
        self.text_cleaner = TextCleaner()
        self.content_analyzer = ContentAnalyzer()
        self.content_router = ContentRouter()

    def process(
        self,
        file_path: str,
    ) -> dict[str, Any]:
        """
        Extract, clean, analyze, and route a document.
        """

        # 1. Extract
        pages = self.document_router.parse(
            file_path
        )

        # 2. Clean
        processed_pages: list[dict] = []

        for page in pages:

            cleaned_text = self.text_cleaner.clean(
                page["text"]
            )

            processed_page = {
                **page,
                "text": cleaned_text,
            }

            processed_pages.append(
                processed_page
            )

        # 3. Analyze
        analysis = self.content_analyzer.analyze(
            processed_pages
        )

        # 4. Route
        routing = self.content_router.route(
            analysis
        )

        return {
            "pages": processed_pages,
            "analysis": analysis,
            "routing": routing,
        }