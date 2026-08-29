import re
import unicodedata


class TextCleaner:
    """
    Enterprise-grade text normalization service.

    Responsibilities:
    - Validate extracted text
    - Normalize Unicode characters
    - Normalize whitespace
    - Preserve paragraph boundaries
    - Repair common PDF line-break artifacts
    - Preserve punctuation and capitalization
    - Avoid destructive semantic modifications

    The cleaner never modifies the original document.
    """

    def clean(self, text: str) -> str:
        """
        Clean and normalize extracted document text.

        Args:
            text: Raw text extracted from a document.

        Returns:
            Cleaned text.

        Raises:
            TypeError: If text is not a string.
            ValueError: If text is empty or contains no usable content.
        """

        self._validate_input(text)

        text = self._normalize_unicode(text)

        text = self._normalize_line_endings(text)

        text = self._repair_hyphenated_line_breaks(text)

        text = self._normalize_spaces(text)

        text = self._normalize_blank_lines(text)

        text = self._remove_line_edge_whitespace(text)

        text = text.strip()

        self._validate_output(text)

        return text

    @staticmethod
    def _validate_input(text: str) -> None:
        """
        Validate input before processing.
        """

        if not isinstance(text, str):
            raise TypeError(
                "Text must be a string."
            )

        if not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )

    @staticmethod
    def _normalize_unicode(text: str) -> str:
        """
        Normalize Unicode characters.

        NFKC helps normalize visually equivalent
        Unicode representations while preserving
        meaningful text.
        """

        return unicodedata.normalize(
            "NFKC",
            text,
        )

    @staticmethod
    def _normalize_line_endings(text: str) -> str:
        """
        Normalize Windows, Mac, and Unix line endings
        to '\\n'.
        """

        return text.replace(
            "\r\n",
            "\n",
        ).replace(
            "\r",
            "\n",
        )

    @staticmethod
    def _repair_hyphenated_line_breaks(text: str) -> str:
        """
        Repair words split across PDF line breaks.

        Example:

            enter-
            prise

        becomes:

            enterprise

        A space is required after the hyphen to avoid
        changing legitimate hyphenated words such as
        'real-time'.
        """

        return re.sub(
            r"(?<=\w)-\n(?=\w)",
            "",
            text,
        )

    @staticmethod
    def _normalize_spaces(text: str) -> str:
        """
        Normalize repeated spaces and tabs.

        Newlines are intentionally preserved because
        they contain document structure.
        """

        return re.sub(
            r"[ \t]+",
            " ",
            text,
        )

    @staticmethod
    def _normalize_blank_lines(text: str) -> str:
        """
        Prevent excessive blank lines while preserving
        paragraph boundaries.
        """

        return re.sub(
            r"\n[ \t]*\n(?:[ \t]*\n)+",
            "\n\n",
            text,
        )

    @staticmethod
    def _remove_line_edge_whitespace(text: str) -> str:
        """
        Remove unnecessary spaces around line boundaries.
        """

        text = re.sub(
            r"[ \t]+\n",
            "\n",
            text,
        )

        text = re.sub(
            r"\n[ \t]+",
            "\n",
            text,
        )

        return text

    @staticmethod
    def _validate_output(text: str) -> None:
        """
        Make sure cleaning did not produce an empty result.
        """

        if not text.strip():
            raise ValueError(
                "Cleaning produced empty text."
            )