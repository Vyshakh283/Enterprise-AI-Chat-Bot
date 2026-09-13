from Backend.app.Services.ingestion.content_router import (
    ContentRouter,
)


router = ContentRouter()


analysis = {
    "total_pages": 4,
    "pages": [
        {
            "page_number": 1,
            "content_type": "text",
        },
        {
            "page_number": 2,
            "content_type": "image",
        },
        {
            "page_number": 3,
            "content_type": "mixed",
        },
        {
            "page_number": 4,
            "content_type": "empty",
        },
    ],
}


result = router.route(analysis)


print("\n========== CONTENT ROUTER TEST ==========")

print(
    f"Total pages: "
    f"{result['total_pages']}"
)

for page in result["pages"]:

    print(
        f"\n--- PAGE {page['page_number']} ---"
    )

    print(
        f"Content type: "
        f"{page['content_type']}"
    )

    print(
        f"Processing strategy: "
        f"{page['processing_strategy']}"
    )