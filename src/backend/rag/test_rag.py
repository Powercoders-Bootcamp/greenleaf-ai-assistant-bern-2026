from .ingest_handbook import ingest_handbook_pdf
from .retriever import HandbookRetriever

from dotenv import load_dotenv
load_dotenv()

result = ingest_handbook_pdf(
    source_path="../../data/raw/Handbook GreenLeaf Logistics.pdf",
    reset_collection=True,
)

print("Ingestion:", result)

retriever = HandbookRetriever()

query = "Can I expense alcohol with client lunch?"
results = retriever.retrieve(query, k=3)

print("Results count:", len(results))

for i, r in enumerate(results, 1):
    print(f"\nResult {i}\n")
    print("TEXT:", r["text"])
    print("METADATA:", r["metadata"])