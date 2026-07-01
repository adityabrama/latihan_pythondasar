# ============================================================
# routers/profile.py
# Router untuk fitur profil milik user sendiri:
# lihat (Read), edit data (Update), upload foto (Update),
# dan hapus akun (Delete).
# ============================================================

import os
import uuid
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import User
from utils import is_valid_email

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Folder tempat menyimpan foto yang diupload.
UPLOAD_DIR = "static/uploads"


# ── LIHAT PROFIL (READ) ────────────────────────────────────
@router.get("/profile/{user_id}", response_class=HTMLResponse)
def view_profile(user_id: int, request: Request, db: Session = Depends(get_db)):
    # SELECT * FROM users WHERE id = user_id LIMIT 1
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    return templates.TemplateResponse(request, "profile.html", {"user": user})


# ── EDIT PROFIL (UPDATE) ───────────────────────────────────
@router.post("/profile/{user_id}/edit")
def edit_profile(
    user_id: int,
    request: Request,
    full_name: str = Form(""),
    email: str = Form(""),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Kalau email diisi, pastikan formatnya valid dulu.
    if email and not is_valid_email(email):
        return templates.TemplateResponse(request, "profile.html", {
            "user": user,
            "photo_error": "Format email tidak valid.",
        })

    # Update atribut user hanya untuk field yang diisi.
    if full_name:
        user.full_name = full_name.strip()
    if email:
        user.email = email.strip()

    db.commit()   # simpan perubahan ke database

    return RedirectResponse(url=f"/profile/{user_id}?updated=1", status_code=303)


# ── UPLOAD FOTO (UPDATE) ───────────────────────────────────
@router.post("/profile/{user_id}/upload-photo")
async def upload_photo(
    user_id: int,
    request: Request,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Validasi: hanya izinkan tipe file gambar.
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if photo.content_type not in allowed_types:
        return templates.TemplateResponse(request, "profile.html", {
            "user": user,
            "photo_error": "File harus berupa gambar (JPG, PNG, GIF, WEBP)",
        })

    # Buat nama file unik dengan UUID supaya tidak bentrok dengan file lain.
    file_extension = photo.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Baca isi file lalu tulis ke disk.
    contents = await photo.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # Hapus foto lama (kalau ada) supaya tidak menumpuk di folder.
    if user.photo:
        old_path = os.path.join(UPLOAD_DIR, user.photo)
        if os.path.exists(old_path):
            os.remove(old_path)

    # Simpan nama file baru ke database.
    user.photo = unique_filename
    db.commit()

    return RedirectResponse(url=f"/profile/{user_id}?updated=1", status_code=303)


# ── HAPUS AKUN SENDIRI (DELETE) ────────────────────────────
@router.post("/profile/{user_id}/delete")
def delete_account(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Hapus foto dari disk kalau ada.
    if user.photo:
        photo_path = os.path.join(UPLOAD_DIR, user.photo)
        if os.path.exists(photo_path):
            os.remove(photo_path)

    db.delete(user)   # tandai objek untuk dihapus
    db.commit()       # eksekusi penghapusan di database

    return RedirectResponse(url="/login", status_code=303)
