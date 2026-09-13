from Backend.app.Services.ingestion.content_analyzer import (
    ContentAnalyzer,
)


analyzer = ContentAnalyzer(
    min_usable_chars=30
)


pages = [
    {
        "page_number": 1,
        "text": (
            "This is a normal enterprise document page "
            "containing sufficient machine-readable text."
        ),
    },
    {
        "page_number": 2,
        "text": "",
        "has_image": True,
    },
    {
        "page_number": 3,
        "text": (
            "This page contains both machine-readable text "
            "and an image."
        ),
        "has_image": True,
    },
    {
        "page_number": 4,
        "text": "",
    },
]


result = analyzer.analyze(pages)


print("\n========== CONTENT ANALYZER TEST ==========")

print(f"Total pages: {result['total_pages']}")

print(
    f"Pages with text: "
    f"{result['pages_with_text']}"
)

print(
    f"Pages with images: "
    f"{result['pages_with_images']}"
)

print(
    f"Pages requiring OCR: "
    f"{result['pages_requiring_ocr']}"
)


for page in result["pages"]:

    print(
        f"\n--- PAGE {page['page_number']} ---"
    )

    print(
        f"Text length: "
        f"{page['text_length']}"
    )

    print(
        f"Has text: "
        f"{page['has_text']}"
    )

    print(
        f"Has image: "
        f"{page['has_image']}"
    )

    print(
        f"Content type: "
        f"{page['content_type']}"
    )

    print(
        f"OCR recommended: "
        f"{page['ocr_recommended']}"
    )