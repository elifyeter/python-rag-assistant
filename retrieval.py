import sqlite3
import json
import numpy as np
from openai import OpenAI

FOUNDRY_URL = "http://127.0.0.1:50446   /v1"  
EMBEDDING_MODEL = "qwen3-embedding-0.6b"
DB_FILE = "rag_database.db"

client = OpenAI(base_url=FOUNDRY_URL, api_key="not-needed")


def get_embedding(text):
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_top_chunks(query, top_k=3):
    """Verilen soruya en alakalı top_k parçayı veritabanından bulur."""

    query_embedding = get_embedding(query)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT source_file, content, embedding FROM chunks")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for source_file, content, embedding_json in rows:
        chunk_embedding = json.loads(embedding_json)
        similarity = cosine_similarity(query_embedding, chunk_embedding)
        results.append((similarity, source_file, content))

    results.sort(key=lambda x: x[0], reverse=True)

    return results[:top_k]


if __name__ == "__main__":
    test_query = "Python'da döngü nasıl yazılır?"
    top_chunks = get_top_chunks(test_query)

    print(f"Soru: {test_query}\n")
    for i, (score, source, content) in enumerate(top_chunks, 1):
        print(f"--- Sonuç {i} (benzerlik: {score:.4f}, kaynak: {source}) ---")
        print(content[:200], "...\n")