from pathlib import Path


class TXTParser:
    """
    Parses plain text documents.

    The parser only reads the original document.
    It does not modify or delete the source file.
    """

    def parse(
        self,
        file_path: str,
    ) -> list[dict]:
        """
        Extract text from a TXT document.

        Returns:
            List containing the document text as page 1.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"TXT file not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        if path.suffix.lower() != ".txt":
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        try:
            text = path.read_text(
                encoding="utf-8-sig"
            )

        except UnicodeDecodeError as exc:
            raise ValueError(
                f"TXT file is not valid UTF-8: {path.name}"
            ) from exc

        except OSError as exc:
            raise RuntimeError(
                f"Failed to read TXT file: {path.name}"
            ) from exc

        return [
            {
                "page_number": 1,
                "text": text.strip(),
            }
        ]