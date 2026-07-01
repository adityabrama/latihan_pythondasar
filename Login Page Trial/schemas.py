# ============================================================
# schemas.py
# Schemas adalah "blueprint" untuk validasi data yang masuk/keluar.
#
# Bedakan dengan models.py:
#   - models.py  -> mendefinisikan struktur DATABASE (tabel).
#   - schemas.py -> mendefinisikan struktur DATA yang dikirim/diterima.
#
# Kita pakai Pydantic. Kelebihannya: kalau tipe data tidak cocok,
# Pydantic otomatis menolak dan memberi pesan error yang jelas.
#
# Catatan: pada aplikasi ini form HTML dikirim lewat Form(...) di router,
# jadi schema di bawah berfungsi sebagai dokumentasi bentuk data +
# bisa dipakai kalau nanti kamu membuat versi API JSON.
# ============================================================

from pydantic import BaseModel


# Schema untuk registrasi user baru (data dari form register).
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: str = ""      # nilai default "" -> field ini opsional


# Schema untuk login. Cukup username dan password.
class UserLogin(BaseModel):
    username: str
    password: str


# Schema untuk admin membuat user dari dashboard root (operasi CREATE).
# Mirip register, tapi admin juga bisa langsung menentukan role.
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str = ""
    role: str = "user"       # "user" atau "admin"


# Schema untuk update data user (operasi UPDATE).
# Semua field opsional (default None) supaya user/admin bisa
# meng-update sebagian data saja tanpa harus mengisi semuanya.
class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    role: str | None = None
