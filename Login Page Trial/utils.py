# ============================================================
# utils.py
# Kumpulan fungsi bantu (helper) kecil yang dipakai di banyak tempat.
# Menaruh fungsi umum di sini membuat kode router lebih bersih dan
# tidak terjadi pengulangan (prinsip DRY: Don't Repeat Yourself).
# ============================================================

import re

# Pola (regex) sederhana untuk mengecek format email.
# Artinya kira-kira: ada teks -> @ -> teks -> titik -> teks.
# Contoh valid: budi@email.com   |  Contoh salah: budi@email
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    """Mengembalikan True kalau format email valid, selain itu False."""
    if not email:
        return False
    return bool(_EMAIL_PATTERN.match(email))


def validate_user_input(username: str, email: str, password: str) -> str | None:
    """
    Memvalidasi input dasar saat membuat/registrasi user.

    Mengembalikan:
      - str berisi pesan error kalau ada yang tidak valid, ATAU
      - None kalau semua input sudah benar.

    Ini contoh 'guard clause': kita cek satu per satu, dan langsung
    kembalikan pesan error begitu menemukan masalah.
    """
    if not username or len(username.strip()) < 3:
        return "Username minimal 3 karakter."

    if not is_valid_email(email):
        return "Format email tidak valid (contoh: nama@email.com)."

    if not password or len(password) < 6:
        return "Password minimal 6 karakter."

    return None  # semua valid
