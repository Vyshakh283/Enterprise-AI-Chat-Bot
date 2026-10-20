from Backend.app.Services.ingestion.content_analyzer import (
    ContentAnalyzer,
)

from Backend.app.Services.ingestion.content_router import (
    ContentRouter,
)


def test_content_routing() -> None:

    analyzer = ContentAnalyzer()
    router = ContentRouter()

    pages = [
        {
            "page_number": 1,
            "text": "Enterprise AI chatbot text content",
        },
        {
            "page_number": 2,
            "text": "",
            "has_image": True,
        },
        {
            "page_number": 3,
            "text": "Text extracted from a page containing an image",
            "has_image": True,
        },
        {
            "page_number": 4,
            "text": "",
        },
    ]

    analysis = analyzer.analyze(pages)

    routing = router.route(analysis)

    print("\n========== CONTENT ANALYSIS ==========")

    for page in analysis["pages"]:
        print(
            f"Page {page['page_number']} → "
            f"{page['content_type']}"
        )

    print("\n========== CONTENT ROUTING ==========")

    for page in routing["pages"]:
        print(
            f"Page {page['page_number']} → "
            f"{page['processing_strategy']}"
        )

    # Page 1 → text
    assert (
        analysis["pages"][0]["content_type"]
        == "text"
    )

    assert (
        routing["pages"][0]["processing_strategy"]
        == "text_processing"
    )

    # Page 2 → image
    assert (
        analysis["pages"][1]["content_type"]
        == "image"
    )

    assert (
        analysis["pages"][1]["ocr_recommended"]
        is True
    )

    assert (
        routing["pages"][1]["processing_strategy"]
        == "ocr"
    )

    # Page 3 → mixed
    assert (
        analysis["pages"][2]["content_type"]
        == "mixed"
    )

    assert (
        routing["pages"][2]["processing_strategy"]
        == "mixed_content_processing"
    )

    # Page 4 → empty
    assert (
        analysis["pages"][3]["content_type"]
        == "empty"
    )

    assert (
        routing["pages"][3]["processing_strategy"]
        == "empty_content"
    )

    print(
        "\nContent analysis and routing test passed."
    )


if __name__ == "__main__":
    test_content_routing()