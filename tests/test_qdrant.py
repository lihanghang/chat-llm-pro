
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient("localhost", port=6333)


def test_qdrant():
    client.recreate_collection(collection_name="doc_embedding",
                               vectors_config=models.VectorParams(
                                   size=1024,
                                   distance=models.Distance.COSINE
                               ),)


print(client)
test_qdrant()
