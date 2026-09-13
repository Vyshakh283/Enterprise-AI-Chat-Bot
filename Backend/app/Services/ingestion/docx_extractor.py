from pathlib import Path

from docx import Document


class DOCXParser:
    """
    Parses Microsoft Word DOCX documents.

    The parser only reads the original document.
    It does not modify or delete the source file.
    """

    def parse(
        self,
        file_path: str,
    ) -> list[dict]:
        """
        Extract text from a DOCX document.

        Returns:
            List containing the extracted document content
            as page 1.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"DOCX file not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        if path.suffix.lower() != ".docx":
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        try:
            document = Document(str(path))

            paragraphs = []

            for paragraph in document.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(
                        paragraph.text
                    )

            text = "\n".join(paragraphs)

        except Exception as exc:
            raise RuntimeError(
                f"Failed to parse DOCX: {path.name}"
            ) from exc

        return [
            {
                "page_number": 1,
                "text": text,
            }
        ]