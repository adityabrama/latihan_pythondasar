# ============================================================
# models.py
# File ini mendefinisikan "bentuk" tabel di database kita.
# Satu class = satu tabel. Inilah yang disebut ORM
# (Object Relational Mapper): kita cukup menulis class Python,
# biar SQLAlchemy yang menerjemahkannya ke perintah SQL.
# ============================================================

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from database import Base


# Class User merepresentasikan tabel bernama "users" di database.
# Setiap atribut (id, username, dll) menjadi satu kolom di tabel.
class User(Base):

    # __tablename__ menentukan nama tabel di database.
    __tablename__ = "users"

    # Kolom angka, menjadi ID unik tiap user (primary key).
    # index=True membuat pencarian berdasarkan ID lebih cepat.
    id = Column(Integer, primary_key=True, index=True)

    # Kolom teks untuk username.
    # unique=True   -> tidak boleh ada dua user dengan username sama.
    # nullable=False -> wajib diisi.
    username = Column(String, unique=True, index=True, nullable=False)

    # Email juga harus unik dan wajib diisi.
    email = Column(String, unique=True, index=True, nullable=False)

    # Password disimpan sebagai teks biasa (plain text) untuk tujuan
    # pembelajaran, sama seperti contoh trainer.
    # CATATAN PENTING: di aplikasi nyata, password WAJIB di-hash
    # (mis. dengan bcrypt) supaya tidak bisa dibaca kalau database bocor.
    password = Column(String, nullable=False)

    # Nama lengkap user, boleh kosong.
    full_name = Column(String, nullable=True)

    # "role" adalah peningkatan dari contoh trainer: menandai apakah
    # user biasa ("user") atau administrator ("admin").
    # Admin nantinya bisa mengelola semua user lewat dashboard root.
    role = Column(String, nullable=False, default="user")

    # Nama file foto profil. Kosong kalau user belum meng-upload foto.
    photo = Column(String, nullable=True)

    # Waktu akun dibuat. default=... membuat SQLAlchemy mengisi kolom ini
    # otomatis saat user baru ditambahkan. Kita pakai waktu UTC yang
    # "timezone-aware" (cara modern, tanpa peringatan deprecation).
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
