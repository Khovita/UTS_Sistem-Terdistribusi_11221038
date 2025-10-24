# UTS Sistem Terdistribusi — Pub-Sub Log Aggregator dengan Idempotent Consumer dan Deduplication

Nama: **Khovita Zulkarimah**  
NIM: **11221038**  
Program Studi: **Informatika, Institut Teknologi Kalimantan**

---

## 🧩 1. Ringkasan Sistem

Sistem ini merupakan layanan **Pub-Sub Log Aggregator** yang menerima event dari *publisher*, lalu memprosesnya melalui *consumer* dengan karakteristik **idempotent** dan **deduplication**. Tujuannya adalah memastikan bahwa setiap event unik hanya diproses **sekali** walaupun dikirim berulang kali (simulasi *at-least-once delivery*).  

Komponen utama sistem terdiri dari:
- **Publisher Endpoint (`/publish`)**: menerima batch event dalam format JSON.
- **Internal Queue (`asyncio.Queue`)**: menyimpan event sementara sebelum diproses.
- **Consumer (background task)**: memproses event dan memeriksa dedup store.
- **Dedup Store (SQLite)**: menyimpan `(topic, event_id)` untuk mencegah reprocessing setelah restart.
- **API Monitoring (`/stats`, `/events`)**: menampilkan data unik, duplikat, dan performa.

Arsitektur ini mengikuti pola **Publish–Subscribe** (Bab 2, Tanenbaum & Van Steen, 2023) dengan fokus pada **idempotency dan consistency** (Bab 7).

---

## ⚙️ 2. Desain Sistem

### a. Arsitektur Umum
- Komunikasi antar komponen bersifat **asynchronous** menggunakan *internal queue*.
- Dedup store berbasis **SQLite** agar tahan restart tanpa dependensi eksternal.
- Consumer bersifat **idempotent**: event dengan `(topic, event_id)` sama diabaikan.
- Ordering tidak total — hanya dijamin per topik (Bab 5: *partial ordering*).

### b. Model Data
```json
{
  "topic": "sensor-data",
  "event_id": "uuid-12345",
  "timestamp": "2025-10-21T10:00:00Z",
  "source": "sensor-1",
  "payload": { "temp": 28.5 }
}
