from typing import Any


class ContentAnalyzer:
    """
    Analyzes extracted document pages.

    Responsibilities:
    - Validate parser output
    - Determine whether usable text exists
    - Detect image metadata when available
    - Classify page content
    - Recommend OCR for image-only pages

    The analyzer does NOT:
    - Parse documents
    - Perform OCR
    - Call VLMs
    - Call IDP systems
    - Modify the original document
    """

    def __init__(self, min_usable_chars: int = 30) -> None:
        if min_usable_chars < 1:
            raise ValueError(
                "min_usable_chars must be greater than 0."
            )

        self.min_usable_chars = min_usable_chars

    def analyze(
        self,
        pages: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not isinstance(pages, list):
            raise TypeError("pages must be a list.")

        if not pages:
            raise ValueError("pages cannot be empty.")

        analyzed_pages: list[dict[str, Any]] = []

        for page in pages:
            analyzed_page = self._analyze_page(page)
            analyzed_pages.append(analyzed_page)

        return {
            "total_pages": len(analyzed_pages),
            "pages_with_text": sum(
                page["has_text"]
                for page in analyzed_pages
            ),
            "pages_with_images": sum(
                page["has_image"]
                for page in analyzed_pages
            ),
            "pages_requiring_ocr": sum(
                page["ocr_recommended"]
                for page in analyzed_pages
            ),
            "pages": analyzed_pages,
        }

    def _analyze_page(
        self,
        page: dict[str, Any],
    ) -> dict[str, Any]:

        if not isinstance(page, dict):
            raise TypeError(
                "Each page must be a dictionary."
            )

        if "page_number" not in page:
            raise ValueError(
                "Page is missing 'page_number'."
            )

        if "text" not in page:
            raise ValueError(
                "Page is missing 'text'."
            )

        page_number = page["page_number"]
        text = page["text"]

        if not isinstance(page_number, int):
            raise TypeError(
                "page_number must be an integer."
            )

        if not isinstance(text, str):
            raise TypeError(
                "page text must be a string."
            )

        text_length = len(text.strip())

        has_text = (
            text_length >= self.min_usable_chars
        )

        has_image = self._detect_image(page)

        if has_text and has_image:
            content_type = "mixed"

        elif has_text:
            content_type = "text"

        elif has_image:
            content_type = "image"

        else:
            content_type = "empty"

        ocr_recommended = (
            not has_text
            and has_image
        )

        return {
            "page_number": page_number,
            "text_length": text_length,
            "has_text": has_text,
            "has_image": has_image,
            "content_type": content_type,
            "ocr_recommended": ocr_recommended,
        }

    @staticmethod
    def _detect_image(
        page: dict[str, Any],
    ) -> bool:

        if "has_image" in page:
            return bool(page["has_image"])

        if "image_count" in page:
            return page["image_count"] > 0

        return False