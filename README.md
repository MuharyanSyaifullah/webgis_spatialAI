# Tugas Praktikum 10 - Spatial AI & Computer Vision untuk WebGIS

## Identitas
- **Nama:** Muharyan Syaifullah
- **NIM:** 123140045

## Deskripsi
Project ini merupakan implementasi **Tugas Praktikum 10 Sistem Informasi Geografis**, yaitu membangun pipeline **Spatial AI** untuk mendeteksi objek pada citra aerial/satelit dan mengintegrasikan hasilnya ke dalam sistem **WebGIS** yang telah dikembangkan sebelumnya.  
Sesuai ketentuan tugas, proses yang dilakukan meliputi pembacaan citra, deteksi objek, pembuatan hasil dalam format **GeoJSON**, penyimpanan ke **PostgreSQL/PostGIS**, dan penampilan hasil deteksi pada peta WebGIS.

## Tujuan
Tujuan project ini adalah:
- menerapkan konsep **Spatial AI** pada data citra,
- menghasilkan data hasil deteksi objek,
- mengubah hasil tersebut menjadi data spasial,
- menyimpan hasil ke database geospasial,
- dan menampilkan hasilnya pada aplikasi WebGIS.

## Fitur
- Input citra aerial/satelit
- Deteksi objek pada citra
- Simpan hasil deteksi ke file **GeoJSON**
- Simpan hasil deteksi ke **PostgreSQL/PostGIS**
- Tampilkan hasil deteksi sebagai layer titik di WebGIS
- Integrasi dengan backend **FastAPI**
- Integrasi dengan frontend **React Leaflet**

## Teknologi yang Digunakan

### Backend
- FastAPI
- Uvicorn
- Psycopg2
- PostgreSQL
- PostGIS

### Frontend
- React
- Vite
- React Leaflet
- Axios

### Spatial AI / Computer Vision
- Python
- OpenCV
- Ultralytics YOLOv8
- Rasterio
- NumPy
- Matplotlib

## Struktur Folder
```text
project/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── webgis-frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── spatial_ai/
│   ├── images/
│   ├── output/
│   ├── detect_pipeline.py
│   └── save_to_postgis.py
└── README.md
```

## Alur Pengerjaan

Alur kerja project ini adalah sebagai berikut:

1. Menyiapkan citra aerial/satelit sebagai input
2. Menjalankan proses deteksi objek pada citra
3. Menyimpan hasil deteksi ke file `detections.geojson`
4. Menyimpan hasil deteksi ke tabel `detections` pada PostgreSQL/PostGIS
5. Menyediakan endpoint backend untuk membaca hasil deteksi dalam format GeoJSON
6. Menampilkan hasil deteksi pada WebGIS sebagai layer tambahan

Alur ini sesuai dengan pipeline yang dijelaskan pada materi pertemuan 10, yaitu **input citra → preprocessing/tiling → deteksi → konversi spasial → GeoJSON/PostGIS → WebGIS**. 

## Persiapan Database

Gunakan database PostgreSQL/PostGIS dengan nama:

```text
sig_123140045
```

### Tabel detections

Jalankan query berikut di pgAdmin:

```sql
CREATE TABLE IF NOT EXISTS detections (
    id SERIAL PRIMARY KEY,
    class_name VARCHAR(100),
    confidence FLOAT,
    geom GEOMETRY(Point, 4326),
    detected_at TIMESTAMP DEFAULT NOW()
);
```

## Cara Menjalankan Spatial AI

Masuk ke folder:

```bash
cd spatial_ai
```

Aktifkan virtual environment.

### PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

### CMD

```cmd
venv\Scripts\activate.bat
```

Install dependency:

```bash
pip install ultralytics opencv-python rasterio numpy matplotlib psycopg2-binary
```

Jalankan pipeline deteksi:

```bash
python detect_pipeline.py
```

Output yang dihasilkan:

* `output/detection_result.jpg`
* `output/detections.geojson`

Simpan hasil ke PostGIS:

```bash
python save_to_postgis.py
```

## Cara Menjalankan Backend

Masuk ke folder backend:

```bash
cd backend
```

Aktifkan virtual environment.

### PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

### CMD

```cmd
venv\Scripts\activate.bat
```

Install dependency:

```bash
pip install fastapi uvicorn psycopg2-binary python-jose[cryptography] passlib[bcrypt]==1.7.4 bcrypt==4.0.1 python-multipart pydantic[email]
```

Jalankan backend:

```bash
python -m uvicorn main:app --reload
```

Backend aktif di:

```text
http://127.0.0.1:8000
```

## Endpoint Backend

Endpoint penting untuk hasil deteksi:

```text
GET /api/detections/geojson
```

Endpoint ini digunakan untuk mengambil hasil deteksi dari tabel `detections` dalam format GeoJSON dan menampilkannya di WebGIS.

## Cara Menjalankan Frontend

Masuk ke folder frontend:

```bash
cd webgis-frontend
```

Install dependency:

```bash
npm install
```

Jalankan frontend:

```bash
npm run dev
```

Jika PowerShell bermasalah:

```bash
npm.cmd run dev
```

Frontend aktif di:

```text
http://localhost:5173
```

## Hasil Akhir

Hasil akhir project ini adalah aplikasi WebGIS yang dapat:

* menampilkan polygon wilayah,
* menampilkan marker fasilitas,
* dan menampilkan hasil deteksi objek sebagai layer tambahan pada peta.

## Catatan

Pada implementasi ini, hasil deteksi objek divisualisasikan dalam bentuk titik dan diintegrasikan ke WebGIS. Materi tugas menekankan bahwa hasil deteksi perlu diekspor ke **GeoJSON** dan ditampilkan di peta WebGIS, yang telah diterapkan pada project ini. 

## Referensi

* Materi Sistem Informasi Geografis Pertemuan 10: **Spatial AI & Computer Vision**