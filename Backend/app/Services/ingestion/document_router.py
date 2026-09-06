from pathlib import Path

from Backend.app.Services.ingestion.pdf_extractor import PDFParser
from Backend.app.Services.ingestion.txt_extractor import TXTParser


class DocumentRouter:
    """
    Routes documents to the appropriate extractor.

    The router decides which parser should handle a document
    based on its file type.
    """

    def __init__(self) -> None:
        self.pdf_parser = PDFParser()
        self.txt_parser = TXTParser()

    def parse(
        self,
        file_path: str,
    ) -> list[dict]:
        """
        Route a document to the appropriate parser.

        Args:
            file_path: Path to the stored document.

        Returns:
            Extracted page-level text.

        Raises:
            FileNotFoundError: If the document does not exist.
            ValueError: If the file type is unsupported.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        extension = path.suffix.lower()

        if extension == ".pdf":
            return self.pdf_parser.parse(file_path)
        
        if extension == ".txt":
            return self.txt_parser.parse(file_path)

        raise ValueError(
            f"Unsupported document type: {extension}"
        )