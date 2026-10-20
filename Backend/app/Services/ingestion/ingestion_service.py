
import logging
from typing import Any

from Backend.app.Services.ingestion.document_router import (
    DocumentRouter,
)
from Backend.app.Services.ingestion.text_cleaner import (
    TextCleaner,
)
from Backend.app.Services.ingestion.content_analyzer import (
    ContentAnalyzer,
)
from Backend.app.Services.ingestion.content_router import (
    ContentRouter,
)
from Backend.app.Services.ingestion.canonicalization_service import (
    CanonicalizationService,
)
from Backend.app.Services.ingestion.processor import (
    ProcessorRegistry,
)

logger = logging.getLogger(__name__)


class IngestionService:
    """
    Coordinates document extraction, processing, and canonicalization.

    This service does not store documents, access the database,
    generate embeddings, or store vectors.
    """

    def __init__(self) -> None:
        self.document_router = DocumentRouter()
        self.text_cleaner = TextCleaner()
        self.content_analyzer = ContentAnalyzer()
        self.content_router = ContentRouter()
        self.processor_registry = ProcessorRegistry()
        self.canonicalization_service = CanonicalizationService()

    def process(
        self,
        file_path: str,
        document_id: str,
    ) -> dict[str, Any]:
        """
        Process a document and return its page-level results.

        Pipeline:
            Extract -> Clean -> Analyze -> Route
            -> Process -> Canonicalize
        """

        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("file_path must be a non-empty string.")

        if not isinstance(document_id, str) or not document_id.strip():
            raise ValueError("document_id must be a non-empty string.")

        # 1. Extract document pages.
        pages = self.document_router.parse(file_path)

        # 2. Clean available extracted text.
        processed_pages: list[dict[str, Any]] = []

        for page in pages:
            raw_text = page.get("text", "")

            if raw_text and raw_text.strip():
                cleaned_text = self.text_cleaner.clean(raw_text)
            else:
                cleaned_text = ""

            processed_pages.append(
                {
                    **page,
                    "text": cleaned_text,
                }
            )

        # 3. Analyze the extracted page content.
        analysis = self.content_analyzer.analyze(processed_pages)

        # 4. Select a processing strategy for each page.
        routing = self.content_router.route(analysis)
        routed_pages = routing["pages"]

        if len(processed_pages) != len(routed_pages):
            raise RuntimeError(
                "Content routing returned a different number of "
                "pages than the document parser."
            )

        # 5. Process each page and create its canonical representation.
        canonical_documents = []

        for page, routed_page in zip(processed_pages, routed_pages):
            page_number = page["page_number"]
            strategy = routed_page["processing_strategy"]

            processor = self.processor_registry.get(strategy)

            # OCR needs the original PDF page, not its empty extracted text.
            if strategy == "ocr":
                processor_input: Any = {
                    "file_path": file_path,
                    "page_number": page_number,
                }
            else:
                processor_input = page["text"]

            processor_result = processor.process(processor_input)

            # Do not let a failed processor result reach canonicalization.
            if processor_result.status != "success":
                error_details = "; ".join(processor_result.errors)
                if not error_details:
                    error_details = (
                        f"Processor status was "
                        f"'{processor_result.status}'."
                    )

                logger.error(
                    "Page processing failed: document_id=%s, "
                    "page_number=%s, strategy=%s, details=%s",
                    document_id,
                    page_number,
                    strategy,
                    error_details,
                )

                raise RuntimeError(
                    f"Document ingestion failed for page {page_number} "
                    f"using strategy '{strategy}': {error_details}"
                )

            canonical_document = (
                self.canonicalization_service.canonicalize(
                    document_id=document_id,
                    page_number=page_number,
                    processor_result=processor_result,
                )
            )

            canonical_documents.append(canonical_document)

        # 6. Return the pipeline results.
        return {
            "document_id": document_id,
            "pages": processed_pages,
            "analysis": analysis,
            "routing": routing,
            "canonical_documents": canonical_documents,
        }
