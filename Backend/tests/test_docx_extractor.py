from Backend.app.Services.ingestion.docx_extractor import DOCXParser


parser = DOCXParser()

file_path = (
    "storage/test_documents/"
    "test_document.docx"
)

pages = parser.parse(file_path)

print(f"Total pages: {len(pages)}")

for page in pages:
    print(
        f"\n========== PAGE {page['page_number']} =========="
    )
    print(f"Text length: {len(page['text'])}")
    print(f"Text repr: {page['text']!r}")