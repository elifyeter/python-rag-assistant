# Python Öğrenme Asistanı - Yerel RAG Uygulaması

Microsoft Foundry Local ve RAG (Retrieval-Augmented Generation) mimarisi kullanarak
geliştirilmiş, tamamen offline çalışan bir soru-cevap chatbot'u.

## Kurulum
1. `pip install -r requirements.txt`
2. Foundry Local'i kurun ve `phi-3.5-mini`, `qwen3-embedding-0.6b` modellerini indirin
3. `python ingest.py` ile dokümanları veritabanına yükleyin
4. `streamlit run app.py` ile arayüzü başlatın

## Kullanılan Teknolojiler
- Microsoft Foundry Local
- SQLite
- Streamlit
- Python

## Demo Video
🎥 Sunum Videosunu İzle https://drive.google.com/file/d/18bpN0dGlqM3uJdrWNebZ2GeueFmFcQD-/view?usp=sharing
