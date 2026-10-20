from pathlib import Path
from typing import cast

import pymupdf


class PDFParser:
    """
    Parses a PDF document page by page.

    The parser only reads the original document.
    It does not modify or delete the source file.

    Responsibilities:
    - Validate PDF file
    - Extract page text
    - Detect embedded images
    - Return page-level metadata

    The parser does NOT:
    - Perform OCR
    - Call an AI model
    - Analyze semantic meaning
    - Route content to OCR/VLM/IDP
    """

    def parse(self, file_path: str) -> list[dict]:
        path = Path(file_path)
        
        if path.suffix.lower() != ".pdf":
                    raise ValueError(
                        f"Unsupported file type: {path.suffix}"
                    )

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )


        pages: list[dict] = []

        try:
            with pymupdf.open(path) as pdf:

                for page_number in range(pdf.page_count):

                    page = pdf.load_page(page_number)

                    text = cast(
                        str,
                        page.get_text("text")
                    ).strip()

                    images = page.get_images(
                        full=True
                    )

                    image_count = len(images)

                    pages.append(
                        {
                            "page_number": page_number + 1,
                            "text": text,
                            "image_count": image_count,
                            "has_image": image_count > 0,
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