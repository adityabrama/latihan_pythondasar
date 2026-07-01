# ============================================================
# app.py
# File utama aplikasi "Login Page Trial".
#
# Cara menjalankan:
#   1. (sekali saja) buat virtual env & install kebutuhan:
#        python -m venv .venv
#        .venv\Scripts\activate        (Windows)
#        pip install -r requirements.txt
#   2. jalankan server:
#        python app.py
#   3. buka browser ke: http://localhost:8000
#
# Struktur fitur (CRUD lengkap):
#   - Dashboard admin di "/"  -> Create, Read, Update, Delete semua user
#   - Register / Login / Profil untuk alur user biasa
# ============================================================

import os
import uvicorn
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

# Import koneksi database + model
from database import engine, SessionLocal
import models
from models import User

# Import router dari tiap modul fitur
from routers import auth, profile, admin

# ── SETUP APLIKASI ─────────────────────────────────────────
app = FastAPI(title="Login Page Trial", version="1.0.0")

# Pastikan folder uploads ada sebelum aplikasi berjalan.
os.makedirs("static/uploads", exist_ok=True)

# Buat semua tabel di database sesuai definisi di models.py.
# Kalau tabel sudah ada, perintah ini diabaikan (data tidak terhapus).
# Setara dengan: CREATE TABLE IF NOT EXISTS ...
models.Base.metadata.create_all(bind=engine)

# Daftarkan folder "static" agar file (foto upload) bisa diakses via URL.
# Contoh: http://localhost:8000/static/uploads/foto.jpg
app.mount("/static", StaticFiles(directory="static"), name="static")

# Gabungkan semua router ke aplikasi utama.
# Urutan include tidak masalah karena path masing-masing berbeda.
app.include_router(admin.router)     # dashboard root "/" + CRUD admin
app.include_router(auth.router)      # /register, /login, /logout
app.include_router(profile.router)   # /profile/...


# ── SEED DATA AWAL ─────────────────────────────────────────
# Supaya dashboard tidak kosong saat pertama kali dijalankan,
# kita buat satu akun admin default + beberapa contoh user.
# Ini hanya berjalan kalau tabel users masih benar-benar kosong.
def seed_initial_data():
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            db.add_all([
                User(username="admin", email="admin@trial.com",
                     password="admin123", full_name="Administrator", role="admin"),
                User(username="budi", email="budi@email.com",
                     password="budi123", full_name="Budi Santoso", role="user"),
                User(username="sari", email="sari@email.com",
                     password="sari123", full_name="Sari Dewi", role="user"),
            ])
            db.commit()
            print(">> Data awal dibuat. Login admin -> username: admin | password: admin123")
    finally:
        db.close()


seed_initial_data()


# ── FAVICON (opsional) ─────────────────────────────────────
# Browser otomatis meminta /favicon.ico. Kita balas "204 No Content"
# supaya tidak memunculkan error 404 yang mengotori log.
@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


# ── JALANKAN SERVER ────────────────────────────────────────
# Blok ini hanya berjalan kalau file dieksekusi langsung (python app.py).
if __name__ == "__main__":
    print("=" * 55)
    print("  Login Page Trial")
    print("  Server berjalan di : http://localhost:8000")
    print("  Dashboard admin    : http://localhost:8000/")
    print("  Login default      : admin / admin123")
    print("  Tekan CTRL+C untuk berhenti")
    print("=" * 55)

    # "app:app" -> file app.py, variabel bernama app
    # reload=True -> server otomatis restart saat kode diubah (mode development)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
