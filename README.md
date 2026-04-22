# WebGIS Full-Stack Tugas 9

## Identitas
- Nama: Muharyan Syaifullah
- NIM: 123140045

## Deskripsi
Project ini merupakan aplikasi WebGIS full-stack yang dibangun menggunakan PostgreSQL/PostGIS, FastAPI, React, dan Leaflet. Aplikasi ini menampilkan wilayah dalam bentuk polygon serta fasilitas publik dalam bentuk marker, dan dilengkapi fitur autentikasi serta CRUD data fasilitas.

## Teknologi yang Digunakan
- PostgreSQL
- PostGIS
- QGIS
- FastAPI
- React + Vite
- React Leaflet
- Axios
- JWT Authentication

## Fitur
- Register
- Login
- Logout
- Menampilkan polygon wilayah
- Menampilkan marker fasilitas
- Tambah fasilitas
- Edit fasilitas
- Hapus fasilitas
- Popup informasi fasilitas
- Data tersimpan di PostgreSQL/PostGIS

## Struktur Project
- backend/
- webgis-frontend/

## Cara Menjalankan Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload