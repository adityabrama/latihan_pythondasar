# ============================================================
# routers/auth.py
# Router adalah cara FastAPI mengelompokkan endpoint yang sejenis.
# File ini khusus menangani AUTENTIKASI: register, login, logout.
#
# Kaitannya dengan CRUD:
#   - register = CREATE (menambah user baru ke database)
#   - login    = READ   (membaca/mencocokkan data user)
# ============================================================

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import User
from utils import validate_user_input

# APIRouter() membuat "sub-router" yang nanti digabungkan di app.py
router = APIRouter()

# Memberitahu FastAPI di mana folder template HTML kita berada.
templates = Jinja2Templates(directory="templates")


# ── REGISTER (CREATE) ──────────────────────────────────────
# @router.get -> merespons HTTP GET (membuka halaman).
# response_class=HTMLResponse -> kita mengembalikan HTML, bukan JSON.
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {})


# @router.post -> merespons HTTP POST (mengirim data form).
@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),     # Form(...) -> ambil data dari form HTML
    email: str = Form(...),        # tanda ... -> field ini WAJIB diisi
    password: str = Form(...),
    full_name: str = Form(""),     # "" -> boleh kosong
    db: Session = Depends(get_db), # Depends(get_db) -> minta sesi DB otomatis
):
    # 1) Validasi format input (username, email, panjang password).
    error = validate_user_input(username, email, password)
    if error:
        return templates.TemplateResponse(request, "register.html", {"error": error})

    # 2) Cek apakah username sudah dipakai.
    #    db.query(User) -> mulai query ke tabel users
    #    .filter(...)   -> tambah kondisi WHERE
    #    .first()       -> ambil satu hasil pertama, atau None kalau tak ada
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse(request, "register.html", {
            "error": "Username sudah digunakan!"
        })

    # 3) Cek apakah email sudah dipakai (peningkatan dari contoh trainer).
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse(request, "register.html", {
            "error": "Email sudah terdaftar!"
        })

    # 4) Buat objek User baru (belum tersimpan ke database).
    new_user = User(
        username=username.strip(),
        email=email.strip(),
        password=password,       # plain text — ingat: hanya untuk pembelajaran!
        full_name=full_name.strip(),
        role="user",
    )

    db.add(new_user)   # masukkan ke antrian penyimpanan
    db.commit()        # simpan permanen ke database

    # Redirect ke halaman login dengan tanda sukses.
    # status_code=303 -> "See Other", pola standar setelah POST berhasil.
    return RedirectResponse(url="/login?success=1", status_code=303)


# ── LOGIN (READ) ───────────────────────────────────────────
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, success: int = 0):
    return templates.TemplateResponse(request, "login.html", {"success": success})


@router.post("/login")
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    # Bersihkan input dari spasi di awal/akhir (sering ikut saat copy-paste
    # atau autofill browser) supaya login tidak gagal gara-gara spasi.
    username = username.strip()
    password = password.strip()

    # Cari user yang username DAN password-nya cocok.
    # func.lower(...) membuat pencocokan username TIDAK peka huruf besar/kecil,
    # jadi "Admin", "ADMIN", dan "admin" dianggap sama.
    user = db.query(User).filter(
        func.lower(User.username) == username.lower(),
        User.password == password,   # perbandingan langsung (plain text)
    ).first()

    if not user:
        return templates.TemplateResponse(request, "login.html", {
            "error": "Username atau password salah!"
        })

    # Login berhasil -> arahkan ke halaman profil user tersebut.
    return RedirectResponse url=f"/profile/{user.id}", stat