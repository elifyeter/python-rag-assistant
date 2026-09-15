import os
import sqlite3
import json
from openai import OpenAI


FOUNDRY_URL = "http://127.0.0.1:60258/v1"
EMBEDDING_MODEL = "qwen3-embedding-0.6b"
DOCUMENTS_FOLDER = "documents"
DB_FILE = "rag_database.db"
CHUNK_SIZE = 500 

client = OpenAI(base_url=FOUNDRY_URL, api_key="not-needed")


def create_database():
    """SQLite veritabanını ve tabloyu oluşturur (yoksa)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT,
            content TEXT,
            embedding TEXT
        )
    """)
    conn.commit()
    return conn


def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Metni yaklaşık chunk_size karakterlik parçalara böler."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def get_embedding(text):
    """Verilen metnin embedding vektörünü Foundry Local'den alır."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def ingest_documents():
    conn = create_database()
    cursor = conn.cursor()

    
    cursor.execute("DELETE FROM chunks")
    conn.commit()

    txt_files = [f for f in os.listdir(DOCUMENTS_FOLDER) if f.endswith(".txt")]
    print(f"{len(txt_files)} adet .txt dosyası bulundu.")

    total_chunks = 0

    for filename in txt_files:
        filepath = os.path.join(DOCUMENTS_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        print(f"  {filename}: {len(chunks)} parçaya bölündü.")

        for chunk in chunks:
            embedding = get_embedding(chunk)
            embedding_json = json.dumps(embedding)  

            cursor.execute(
                "INSERT INTO chunks (source_file, content, embedding) VALUES (?, ?, ?)",
                (filename, chunk, embedding_json)
            )
            total_chunks += 1

    conn.commit()
    conn.close()
    print(f"\nToplam {total_chunks} parça veritabanına kaydedildi. ({DB_FILE})")


if __name__ == "__main__":
    ingest_documents()