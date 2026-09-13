from typing import Any


class ContentRouter:
    """
    Routes analyzed document pages to the appropriate
    downstream processing strategy.

    The router makes a processing decision only.
    It does not perform OCR, IDP, VLM, or other processing.
    """

    def route(
        self,
        analysis: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create processing decisions for analyzed pages.
        """

        if not isinstance(analysis, dict):
            raise TypeError("analysis must be a dictionary.")

        if "pages" not in analysis:
            raise ValueError(
                "analysis is missing 'pages'."
            )

        pages = analysis["pages"]

        if not isinstance(pages, list):
            raise TypeError(
                "analysis['pages'] must be a list."
            )

        routed_pages: list[dict[str, Any]] = []

        for page in pages:
            routed_page = self._route_page(page)
            routed_pages.append(routed_page)

        return {
            "total_pages": len(routed_pages),
            "pages": routed_pages,
        }

    def _route_page(
        self,
        page: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Determine the next processing strategy
        for one page.
        """

        if not isinstance(page, dict):
            raise TypeError(
                "Each page must be a dictionary."
            )

        if "page_number" not in page:
            raise ValueError(
                "Page is missing 'page_number'."
            )

        if "content_type" not in page:
            raise ValueError(
                "Page is missing 'content_type'."
            )

        page_number = page["page_number"]
        content_type = page["content_type"]

        if not isinstance(page_number, int):
            raise TypeError(
                "page_number must be an integer."
            )

        if content_type == "text":
            processing_strategy = "text_processing"

        elif content_type == "image":
            processing_strategy = "ocr"

        elif content_type == "mixed":
            processing_strategy = "mixed_content_processing"

        elif content_type == "empty":
            processing_strategy = "empty_content"

        else:
            raise ValueError(
                f"Unsupported content type: {content_type}"
            )

        return {
            "page_number": page_number,
            "content_type": content_type,
            "processing_strategy": processing_strategy,
        }