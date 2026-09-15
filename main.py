import sqlite3
import json
import numpy as np
from openai import OpenAI

FOUNDRY_URL = "http://127.0.0.1:50446/v1"  
CHAT_MODEL = "phi-3.5-mini"
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


def answer_query(user_question):
    """RAG pipeline'ının tamamı: retrieval + generation."""

    top_chunks = get_top_chunks(user_question, top_k=3)

    best_score = top_chunks[0][0]
    SIMILARITY_THRESHOLD = 0.5  

    if best_score < SIMILARITY_THRESHOLD:
        return "Bu bilgi elimdeki dokümanlarda yok. Sadece Python temel konuları hakkında (fonksiyonlar, döngüler, listeler, sözlükler, hata yönetimi vb.) soru sorabilirsiniz."

    context_text = "\n\n---\n\n".join(
        [f"[Kaynak: {source}]\n{content}" for _, source, content in top_chunks]
    )

    system_prompt = (
        "Sen yardımsever bir Python öğretmeni asistanısın. "
        "Sadece sana verilen bağlam (context) bilgisini kullanarak soruları cevapla. "
        "Eğer cevap bağlamda yoksa, 'Bu bilgi elimdeki dokümanlarda yok' de. "
        "Cevaplarını Türkçe ve anlaşılır şekilde ver."
    )

    user_prompt = f"""Bağlam:
{context_text}

Soru: {user_question}"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content


def main():
    print("=== Python Öğrenme Asistanı ===")
    print("Çıkmak için 'exit' yazın.\n")

    while True:
        user_question = input("Soru: ")
        if user_question.lower() in ["exit", "quit", "çık"]:
            break

        answer = answer_query(user_question)
        print(f"\nCevap: {answer}\n")


if __name__ == "__main__":
    main()