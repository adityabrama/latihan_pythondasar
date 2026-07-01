# 🔐 Login Page Trial

Latihan membuat sistem **Login + Manajemen User** dengan **FastAPI**, terinspirasi
dari contoh trainer, tapi ditingkatkan dengan **Dashboard Admin ber-CRUD penuh** di
halaman root (`/`).

Semua kode diberi komentar Bahasa Indonesia supaya mudah dipelajari.

---

## ✨ Fitur

- **Dashboard Admin (root `/`)** — menampilkan seluruh user dalam tabel, lengkap dengan
  pencarian dan tombol aksi. Di sinilah **CRUD** lengkap berada.
- **Register & Login** — alur user biasa (daftar akun lalu masuk).
- **Profil User** — lihat, edit data, upload foto, dan hapus akun sendiri.
- **Validasi input** — username minimal 3 karakter, format email dicek, password minimal 6 karakter.
- **Role user/admin** — tiap user punya peran yang bisa diatur.
- **Data awal otomatis** — 1 admin + 2 contoh user dibuat saat pertama dijalankan.

---

## 🗺️ Peta CRUD (yang diminta: Create, Read, Update, Delete di root)

| Operasi    | Aksi di aplikasi                     | Endpoint                         |
|------------|--------------------------------------|----------------------------------|
| **Create** | Tambah user dari dashboard           | `GET /admin/new`, `POST /admin/create` |
| **Read**   | Daftar semua user + detail satu user | `GET /` , `GET /admin/{id}`      |
| **Update** | Edit data user                       | `GET /admin/{id}/edit`, `POST /admin/{id}/edit` |
| **Delete** | Hapus user                           | `POST /admin/{id}/delete`        |

Alur autentikasi tambahan: `register` = Create, `login` = Read,
edit/upload foto di profil = Update, hapus akun = Delete.

---

## 📁 Struktur Folder

```
Login Page Trial/
├── app.py              # Entry point: setup app, mount, router, seed data awal
├── database.py         # Koneksi SQLite + sesi database
├── models.py           # Model tabel User (ORM SQLAlchemy)
├── schemas.py          # Blueprint validasi data (Pydantic)
├── utils.py            # Fungsi bantu: validasi email & input
├── routers/
│   ├── auth.py         # register, login, logout
│   ├── profile.py      # profil sendiri: read, update, upload foto, delete
│   └── admin.py        # DASHBOARD ROOT: CRUD penuh atas semua user
├── templates/
│   ├── base.html       # Layout + CSS bersama
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── dashboard.html  # tabel semua user (root)
│   ├── admin_create.html
│   └── admin_edit.html
├── static/uploads/     # tempat foto profil tersimpan
└── requirements.txt
```

---

## 🚀 Cara Menjalankan

Dari dalam folder `Login Page Trial`:

```bash
# 1. (sekali saja) buat virtual environment
python -m venv .venv

# 2. aktifkan virtual environment
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. install kebutuhan
pip install -r requirements.txt

# 4. jalankan server
python app.py
```

Lalu buka **http://localhost:8000** di browser.

**Login admin default:** `admin` / `admin123`

---

## 🧠 Yang Bisa Dipelajari

- Memisahkan kode menjadi beberapa file (models, schemas, routers) agar rapi.
- Konsep **ORM**: menulis class Python, SQLAlchemy yang urus SQL-nya.
- Membuat endpoint **GET** (menampilkan halaman) dan **POST** (memproses form).
- Pola **Redirect setelah POST** (status 303) supaya form tidak terkirim dua kali.
- Validasi input dan penanganan error yang ramah pengguna.

---

## ⚠️ Catatan Penting (Keamanan)

Aplikasi ini dibuat untuk **belajar**, jadi ada beberapa hal yang **belum aman untuk produksi**:

1. **Password disimpan sebagai teks biasa.** Di dunia nyata wajib di-*hash* (mis. `bcrypt`).
2. **Dashboard admin belum dilindungi login.** Idealnya hanya user ber-role `admin`
   dan sudah login yang boleh mengaksesnya (butuh session/cookie).

Kedua hal ini adalah bahan latihan lanjutan yang bagus untuk ditambahkan sendiri. 🙂
