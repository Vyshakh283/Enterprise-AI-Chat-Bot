from Backend.app.Models.user import User
from Backend.app.Models.Document import Document
from Backend.app.Models.Document_chunks import document_chunks
from Backend.app.Models.Embedding_model import Embedding

from Backend.app.database.base import Base


print("\n========== MODEL REGISTRY ==========")

print("User class:", User)
print("Document class:", Document)
print("DocumentChunk class:", document_chunks)
print("Embedding class:", Embedding)

print("\n========== BASE REGISTRY ==========")

for name, cls in Base.registry._class_registry.items():
    print("REGISTERED:", name, "->", cls)

print("\n========== REGISTRY CHECK ==========")

print("User registered:",
      "User" in Base.registry._class_registry)

print("Document registered:",
      "Document" in Base.registry._class_registry)

print("document_chunks registered:",
      "document_chunks" in Base.registry._class_registry)

print("Embedding registered:",
      "Embedding" in Base.registry._class_registry)