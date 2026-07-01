# ============================================================
# database.py
# File ini bertugas membuat koneksi ke database SQLite
# dan menyediakan "sesi" yang dipakai untuk query data.
#
# Analogi: kalau database itu gudang, maka:
#   - engine   = pintu + jalan menuju gudang
#   - session  = petugas yang mengambil/menaruh barang
#   - Base     = cetakan/blueprint untuk rak-rak (tabel)
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# URL koneksi ke database SQLite.
# "sqlite:///./data.db" artinya: buat file bernama data.db
# di folder yang sama dengan project kita.
DATABASE_URL = "sqlite:///./data.db"

# Engine adalah "mesin" yang menangani komunikasi ke database.
# connect_args di bawah khusus untuk SQLite supaya engine-nya
# aman dipakai oleh banyak thread (FastAPI bisa menangani banyak
# request sekaligus).
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal adalah "pabrik" untuk membuat sesi database.
# Setiap request dari user akan mendapat satu sesi sendiri,
# jadi data antar-user tidak saling tercampur.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base adalah kelas induk untuk semua model/tabel kita.
# Setiap tabel yang kita buat WAJIB mewarisi (inherit) dari Base ini
# supaya SQLAlchemy tahu bahwa class tersebut adalah sebuah tabel.
class Base(DeclarativeBase):
    pass


# Fungsi ini dipanggil otomatis setiap kali ada request masuk
# (lewat Depends(get_db) di router).
# Tugasnya: buka sesi -> pinjamkan ke handler -> tutup sesi setelah selesai.
# Kata kunci "yield" membuat fungsi ini menjadi "generator":
# ia berhenti sejenak di baris yield, menyerahkan db, lalu melanjutkan
# ke blok finally saat request selesai.
def get_db():
    db = SessionLocal()
    try:
        yield db          # pinjamkan sesi ke fungsi yang meminta
    finally:
        db.close()        # selalu tutup sesi, walau terjadi error
