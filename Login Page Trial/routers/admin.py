# ============================================================
# routers/admin.py
# INI BAGIAN UTAMA PERMINTAAN: dashboard "root" dengan CRUD penuh.
#
# Dashboard ini berada di halaman utama ("/") dan memungkinkan kita
# mengelola SEMUA user:
#   - CREATE : tambah user baru            -> POST /admin/create
#   - READ   : lihat daftar & detail user  -> GET  /  dan  GET /admin/{id}
#   - UPDATE : ubah data user              -> POST /admin/{id}/edit
#   - DELETE : hapus user                  -> POST /admin/{id}/delete
#
# CATATAN KEAMANAN (edukatif):
# Di aplikasi nyata, halaman admin ini HARUS dilindungi (hanya boleh
# diakses user dengan role "admin" dan yang sudah login). Karena contoh
# ini belum memakai session/cookie, dashboard sengaja dibuat terbuka
# supaya mudah dipelajari. Jangan dipakai apa adanya di produksi.
# ============================================================

import os
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from models import User
from utils import validate_user_input, is_valid_email

router = APIRouter()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "static/uploads"


# ── DASHBOARD / DAFTAR USER (READ semua) ───────────────────
# Ini endpoint "root". Membuka http://localhost:8000/ akan
# menampilkan tabel berisi seluruh user + tombol aksi CRUD.
@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, q: str = "", db: Session = Depends(get_db)):
    # Mulai query dasar: ambil semua user.
    query = db.query(User)

    # Kalau ada kata kunci pencarian (q), saring berdasarkan
    # username ATAU email yang mengandung kata tersebut.
    # or_(...) = kondisi WHERE ... OR ... di SQL.
    if q:
        keyword = f"%{q}%"
        query = query.filter(or_(User.username.like(keyword),
                                 User.email.like(keyword)))

    # Urutkan dari yang ID-nya terbesar (user terbaru di atas).
    users = query.order_by(User.id.desc()).all()

    return templates.TemplateResponse(request, "dashboard.html", {
        "users": users,
        "q": q,
        "total": db.query(User).count(),   # total user untuk statistik
    })


# ── DETAIL SATU USER (READ satu) ───────────────────────────
# Perhatikan "{user_id:int}": tambahan ":int" membuat rute ini HANYA
# cocok kalau bagian URL berupa angka. Jadi "/admin/new" (huruf) tidak
# akan salah masuk ke sini, melainkan ke rute form tambah user di bawah.
@router.get("/admin/{user_id:int}", response_class=HTMLResponse)
def admin_view_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return templates.TemplateResponse(request, "profile.html", {
        "user": user,
        "from_admin": True,   # supaya template tahu ada tombol "kembali ke dashboard"
    })


# ── FORM TAMBAH USER (CREATE - tampilkan form) ─────────────
@router.get("/admin/new", response_class=HTMLResponse)
def create_user_form(request: Request):
    return templates.TemplateResponse(request, "admin_create.html", {})


# ── PROSES TAMBAH USER (CREATE - simpan) ───────────────────
@router.post("/admin/create")
def create_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(""),
    role: str = Form("user"),
    db: Session = Depends(get_db),
):
    # Validasi input dasar.
    error = validate_user_input(username, email, password)
    if error:
        return templates.TemplateResponse(request, "admin_create.html", {
            "error": error,
            # kirim balik nilai yang tadi diketik supaya form tidak kosong lagi
            "form": {"username": username, "email": email,
                     "full_name": full_name, "role": role},
        })

    # Cek username & email unik.
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse(request, "admin_create.html", {
            "error": "Username sudah digunakan!",
            "form": {"username": username, "email": email,
                     "full_name": full_name, "role": role},
        })
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse(request, "admin_create.html", {
            "error": "Email sudah terdaftar!",
            "form": {"username": username, "email": email,
                     "full_name": full_name, "role": role},
        })

    # Pastikan role hanya "user" atau "admin".
    if role not in ("user", "admin"):
        role = "user"

    new_user = User(
        username=username.strip(),
        email=email.strip(),
        password=password,
        full_name=full_name.strip(),
        role=role,
    )
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/?created=1", status_code=303)


# ── FORM EDIT USER (UPDATE - tampilkan form) ───────────────
@router.get("/admin/{user_id:int}/edit", response_class=HTMLResponse)
def edit_user_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return templates.TemplateResponse(request, "admin_edit.html", {"user": user})


# ── PROSES EDIT USER (UPDATE - simpan) ─────────────────────
@router.post("/admin/{user_id:int}/edit")
def edit_user(
    user_id: int,
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(""),
    role: str = Form("user"),
    password: str = Form(""),   # kosong = password tidak diubah
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Validasi format email.
    if not is_valid_email(email):
        return templates.TemplateResponse(request, "admin_edit.html", {
            "user": user,
            "error": "Format email tidak valid.",
        })

    # Cek username unik, TAPI abaikan user ini sendiri (User.id != user_id).
    dup = db.query(User).filter(User.username == username,
                                User.id != user_id).first()
    if dup:
        return templates.TemplateResponse(request, "admin_edit.html", {
            "user": user,
            "error": "Username sudah dipakai user lain.",
        })

    # Cek email unik dengan cara yang sama.
    dup_email = db.query(User).filter(User.email == email,
                                      User.id != user_id).first()
    if dup_email:
        return templates.TemplateResponse(request, "admin_edit.html", {
            "user": user,
            "error": "Email sudah dipakai user lain.",
        })

    # Terapkan perubahan.
    user.username = username.strip()
    user.email = email.strip()
    user.full_name = full_name.strip()
    user.role = role if role in ("user", "admin") else "user"

    # Password hanya diganti kalau field-nya diisi.
    if password:
        user.password = password

    db.commit()

    return RedirectResponse(url="/?updated=1", status_code=303)


# ── HAPUS USER (DELETE) ────────────────────────────────────
@router.post("/admin/{user_id:int}/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Ikut hapus file foto dari disk supaya tidak ada file yatim.
    if user.photo:
        photo_path = os.path.join(UPLOAD_DIR, user.photo)
        if os.path.exists(photo_path):
            os.remove(photo_path)

    db.delete(user)
    db.commit()

    return RedirectResponse(url="/?deleted=1", status_code=303)
