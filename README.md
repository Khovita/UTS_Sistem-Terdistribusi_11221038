# UTS Sistem Terdistribusi — Pub-Sub Log Aggregator

## Deskripsi
Sistem **Pub-Sub Log Aggregator** yang menerima event dari publisher dan memproses melalui idempotent consumer dengan deduplication berbasis SQLite. Dirancang untuk memastikan *exactly-once effect* menggunakan *at-least-once delivery*.

## Deskripsi
Link Youtube: https://youtu.be/eHLOr-2wJCg
---

## Cara Menjalankan

### 1. Build Docker Image
docker build -t uts-aggregator .

### 2. Build Docker Image
docker run -d -p 8080:8080 -v "%cd%/data:/app/data" uts-aggregator

### 3. Cek dedup_store.db di folder /data


### 4. Buka Swagger UI
http://localhost:8080/docs

### 5. Kirim Event Pertama
Klik POST /publish → Try it out
Klik Execute
Lalu buka GET /stats
Klik Execute

### 6. Uji Duplikasi
Ulangi langkah 5 dan kirim event yang sama lagi

### 7. Uji persisten
docker ps
docker stop <container_id>

docker run -d -p 8080:8080 -v "%cd%/data:/app/data" uts-aggregator

### 8. 
kirim ulang event yang sama

buka /stats
