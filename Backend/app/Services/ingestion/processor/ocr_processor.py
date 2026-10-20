
import logging
import tempfile
from pathlib import Path
from statistics import mean
from typing import Any

import pymupdf
from paddleocr import PaddleOCR

from Backend.app.Services.ingestion.processor.base_processor import (
    BaseProcessor,
)
from Backend.app.Services.ingestion.processor.processor_result import (
    ProcessorResult,
)

logger = logging.getLogger(__name__)


class OCRProcessor(BaseProcessor):
    """
    Extract text from scanned PDF pages using PaddleOCR.

    Expected input:
        {
            "file_path": "storage/documents/example.pdf",
            "page_number": 1,
        }

    PaddleOCR is initialized lazily and reused across pages.
    """

    def __init__(
        self,
        language: str = "en",
        device: str = "cpu",
        render_scale: float = 2.0,
        min_confidence: float = 0.30,
    ) -> None:
        if render_scale <= 0:
            raise ValueError("render_scale must be greater than zero.")

        if not 0.0 <= min_confidence <= 1.0:
            raise ValueError(
                "min_confidence must be between 0.0 and 1.0."
            )

        self.language = language
        self.device = device
        self.render_scale = render_scale
        self.min_confidence = min_confidence
        self._ocr: PaddleOCR | None = None

    def _get_ocr_engine(self) -> PaddleOCR:
        """Create the OCR engine only when OCR is first needed."""
        if self._ocr is None:
            logger.info(
                "Initializing PaddleOCR: language=%s, device=%s",
                self.language,
                self.device,
            )
            self._ocr = PaddleOCR(
                lang=self.language,
                device=self.device,
            )

        return self._ocr

    @staticmethod
    def _extract_result_data(result: Any) -> dict[str, Any]:
        """Normalize PaddleOCR's result representation."""
        data = getattr(result, "json", None)

        if callable(data):
            data = data()

        if not isinstance(data, dict):
            return {}

        # PaddleOCR 3.x commonly wraps recognition data in "res".
        nested = data.get("res")
        if isinstance(nested, dict):
            return nested

        return data

    def process(self, content: Any) -> ProcessorResult:
        if not isinstance(content, dict):
            raise ValueError(
                "OCR content must be a dictionary containing "
                "'file_path' and 'page_number'."
            )

        file_path_value = content.get("file_path")
        page_number = content.get("page_number")

        if not isinstance(file_path_value, (str, Path)):
            raise ValueError("'file_path' must be a string or Path.")

        if (
            isinstance(page_number, bool)
            or not isinstance(page_number, int)
            or page_number < 1
        ):
            raise ValueError("'page_number' must be a positive integer.")

        file_path = Path(file_path_value)

        if not file_path.is_file():
            raise FileNotFoundError(
                f"OCR source PDF does not exist: {file_path}"
            )

        if file_path.suffix.lower() != ".pdf":
            raise ValueError("OCR currently supports PDF pages only.")

        try:
            # Render the requested PDF page to a temporary image.
            # The original uploaded document remains unchanged.
            with pymupdf.open(file_path) as pdf:
                if page_number > len(pdf):
                    raise ValueError(
                        f"Page {page_number} is outside the PDF's "
                        f"page range (1-{len(pdf)})."
                    )

                page = pdf[page_number - 1]
                pixmap = page.get_pixmap(
                    matrix=pymupdf.Matrix(
                        self.render_scale,
                        self.render_scale,
                    ),
                    colorspace=pymupdf.csRGB,
                    alpha=False,
                )

                with tempfile.NamedTemporaryFile(
                    suffix=".png",
                    delete=False,
                ) as temp_file:
                    image_path = Path(temp_file.name)

                try:
                    pixmap.save(str(image_path))
                finally:
                    pixmap = None

            try:
                engine = self._get_ocr_engine()
                predictions = engine.predict(input=str(image_path))
            finally:
                image_path.unlink(missing_ok=True)

            lines: list[dict[str, Any]] = []
            warnings: list[str] = []

            for prediction in predictions:
                data = self._extract_result_data(prediction)

                texts = data.get("rec_texts", [])
                scores = data.get("rec_scores", [])

                if not isinstance(texts, list):
                    continue

                if not isinstance(scores, list):
                    scores = []

                for index, raw_text in enumerate(texts):
                    if not isinstance(raw_text, str):
                        continue

                    text = raw_text.strip()
                    if not text:
                        continue

                    score: float | None = None

                    if index < len(scores):
                        try:
                            score = float(scores[index])
                        except (TypeError, ValueError):
                            score = None

                    if score is not None and not 0.0 <= score <= 1.0:
                        score = None

                    if (
                        score is not None
                        and score < self.min_confidence
                    ):
                        continue

                    lines.append(
                        {
                            "text": text,
                            "confidence": score,
                        }
                    )

            extracted_text = "\n".join(
                line["text"] for line in lines
            )

            confidence_values = [
                line["confidence"]
                for line in lines
                if line["confidence"] is not None
            ]

            overall_confidence = (
                mean(confidence_values)
                if confidence_values
                else None
            )

            if not extracted_text:
                warnings.append(
                    "OCR completed but did not recognize usable text."
                )
            elif overall_confidence is None:
                warnings.append(
                    "OCR did not provide usable confidence scores."
                )

            logger.info(
                "OCR completed for page %s of %s; recognized lines=%s",
                page_number,
                file_path.name,
                len(lines),
            )

            return ProcessorResult(
                status="success",
                processor="ocr",
                content_type="image",
                text=extracted_text,
                structured_data={"lines": lines},
                metadata={
                    "engine": "PaddleOCR",
                    "language": self.language,
                    "device": self.device,
                    "source_file": file_path.name,
                    "page_number": page_number,
                    "recognized_line_count": len(lines),
                    "min_confidence": self.min_confidence,
                },
                confidence=overall_confidence,
                warnings=warnings,
                errors=[],
            )

        except Exception as exc:
            logger.exception(
                "OCR failed for file %s, page %s",
                file_path.name,
                page_number,
            )

            return ProcessorResult(
                status="failed",
                processor="ocr",
                content_type="image",
                text=None,
                structured_data={},
                metadata={
                    "source_file": file_path.name,
                    "page_number": page_number,
                },
                confidence=None,
                warnings=[],
                errors=[f"OCR processing failed: {exc}"],
            )
