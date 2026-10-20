
from pathlib import Path

import pymupdf
from paddleocr import PaddleOCR


def main() -> None:
    pdf_path = Path(
        "storage/documents/4/37fc4e03-2ffe-476b-b7a0-d2f19364f455/CV(UPDATED).pdf"
    )

    if not pdf_path.is_file():
        raise FileNotFoundError(f"Test PDF not found: {pdf_path}")

    # Render the first PDF page into an image.
    with pymupdf.open(pdf_path) as pdf:
        if len(pdf) == 0:
            raise ValueError("The PDF contains no pages.")

        page = pdf[0]
        pixmap = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2),
            colorspace=pymupdf.csRGB,
            alpha=False,
        )
        image_path = Path("storage/test_ocr_page.png")
        image_path.parent.mkdir(parents=True, exist_ok=True)
        pixmap.save(image_path)

    print(f"Rendered page to: {image_path}")

    # Initialize the English OCR pipeline.
    # First initialization may download model weights.
    ocr = PaddleOCR(
        lang="en",
        device="cpu",
    )

    results = ocr.predict(input=str(image_path))

    for result in results:
        result.print()
        data = result.json
        print("OCR result:", data)


if __name__ == "__main__":
    main()
