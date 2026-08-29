from pathlib import Path
from typing import cast

import pymupdf

class PDFParser:
    
    """
    Parses a PDF document page by page.

    The parser only reads the original document.
    It does not modify or delete the source file.
    """

    def parse(
        self,
        file_path: str,
    ) -> list[dict]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        pages: list[dict] = []

        try:

            with pymupdf.open(path) as pdf:

                for page_number in range(
                    pdf.page_count
                ):

                    page = pdf.load_page(
                        page_number
                    )

                    text = cast(str, page.get_text("text")).strip()                  
                    pages.append(
                        {
                            "page_number": page_number + 1,
                            "text": text,
                        }
                    )

        except Exception as exc:

            raise RuntimeError(
                f"Failed to parse PDF: {path.name}"
            ) from exc

        if not pages:
            raise ValueError(
                f"PDF contains no pages: {path.name}"
            )

        return pages