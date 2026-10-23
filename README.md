# 🐍 Python Öğrenme Asistanı

**Offline RAG Tabanlı Doküman Soru-Cevap Sistemi**

Python temel konuları hakkında soru sorulabilen, dokümanlardan ilgili bilgileri bulup yerel bir LLM kullanarak cevap üreten bir soru-cevap uygulamasıdır.

## Projenin Amacı

Bu projede **RAG (Retrieval-Augmented Generation)** yaklaşımı kullanılarak, Python dokümanlarından soruyla ilgili bilgilerin bulunması ve bu bilgiler doğrultusunda cevap oluşturulması amaçlanmıştır.

Sistem **Microsoft Foundry Local** kullanılarak yerel olarak çalışacak şekilde tasarlanmıştır.

## Sistem Nasıl Çalışıyor?

1. Kullanıcının sorusu alınır.
2. Sorunun embedding'i oluşturulur.
3. SQLite veritabanındaki doküman embeddingleriyle benzerlik karşılaştırması yapılır.
4. **Cosine Similarity** kullanılarak soruyla en alakalı doküman parçaları bulunur.
5. Bulunan içerikler, kullanıcı sorusuyla birlikte yerel LLM'e gönderilir.
6. LLM, verilen doküman içeriklerine göre cevabı oluşturur.

Dokümanlarda soruyla ilgili yeterli bilgi bulunmadığında sistem cevap uydurmak yerine kullanıcıya bilgi bulunamadığını bildirir.

## Kullanılan Teknolojiler

* **Python** – Ana programlama dili
* **Microsoft Foundry Local** – Yerel LLM ve embedding modelleri
* **Qwen3 Embedding 0.6B** – Metinleri embedding vektörlerine dönüştürme
* **Phi-3.5 Mini** – Cevap üretme
* **SQLite** – Doküman ve embedding verilerini saklama
* **NumPy** – Vektör işlemleri
* **Cosine Similarity** – Benzerlik hesaplama
* **Streamlit** – Web arayüzü

## Proje Yapısı

```text
documents/
├── Python dokümanları

app.py
├── Streamlit web arayüzü

ingest.py
├── Dokümanları işleme ve veritabanına aktarma

retrieval.py
├── İlgili doküman parçalarını bulma

main.py
├── Terminal üzerinden soru-cevap

requirements.txt
├── Gerekli Python paketleri
```

## Kullanım

Gerekli Python paketlerini yüklemek için:

```bash
pip install -r requirements.txt
```

Web arayüzünü başlatmak için:

```bash
streamlit run app.py
```

Uygulama açıldıktan sonra Python temel konuları hakkında sorular sorulabilir ve cevap oluşturulurken kullanılan kaynaklar görüntülenebilir.
