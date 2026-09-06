from Backend.app.Services.ingestion.ingestion_service import IngestionService


service = IngestionService()


pdf_path = (
    "storage/documents/4/"
    "ccca9aad-3217-4c1c-b466-c0b4f6303577/"
    "t1.pdf"
)

txt_path = "storage/test_documents/test_text.txt"


print("\n========== PDF TEST ==========")

pdf_pages = service.process(pdf_path)

print(f"Total processed pages: {len(pdf_pages)}")

for page in pdf_pages:
    print(f"\n--- PAGE {page['page_number']} ---")
    print(repr(page["text"]))


print("\n========== TXT TEST ==========")

txt_pages = service.process(txt_path)

print(f"Total processed pages: {len(txt_pages)}")

for page in txt_pages:
    print(f"\n--- PAGE {page['page_number']} ---")
    print(repr(page["text"]))