#TUGAS TRY
#Buatlah sebuah program Python untuk mensimulasikan sistem kasir pintar di toko daging. Program harus berjalan dengan ketentuan sebagai berikut:
#1. Pricelist: Simpan data harga daging menggunakan struktur data Dictionary dengan varian: #Ayam (Rp15.000/kg), Sapi (Rp12.000/kg), dan Babi (Rp10.000/kg).
#2. Perulangan: Gunakan while loop agar sistem terus menerus menanyakan daging apa yang ingin dibeli sampai pengguna mengetik kata "cukup".
#3. Input & Validasi: Sistem menerima input jenis daging dan jumlah kilogram yang dibeli (bisa desimal). Jika jenis daging tidak terdaftar, berikan pesan peringatan aman.
#4. Logika Diskon Bersarang (Nested IF): Hitung diskon secara otomatis di dalam perulangan untuk setiap item yang berhasil diinput dengan aturan:
    #1. Jika membeli Ayam minimal 5 kg, dapatkan diskon 10% dari subtotal ayam tersebut.
    #2. Jika membeli Sapi minimal 2 kg, dapatkan diskon 15% dari subtotal sapi tersebut.
    #3. Jika membeli Babi minimal 3 kg, dapatkan diskon 12% dari subtotal babi tersebut.
#5. Output: Setelah perulangan berhenti, cetak nota pembayaran secara rapi yang menampilkan total kotor seluruh belanjaan, total potongan diskon yang didapatkan, dan total bersih yang harus dibayar.
import json
import os

# FUNCTION 1: Membaca data pricelist
def muat_menu():
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "menu.json")
    with open(path, "r") as file:
        return json.load(file)

# FUNCTION 2: Menghitung diskon
def hitung_diskon(daging, kg, subtotal, data_diskon):
    if daging in data_diskon:
        aturan = data_diskon[daging]
        if kg >= aturan["min_kg"]:
            return subtotal * aturan["persen"]
    return 0

# FUNCTION 3: Mencetak nota pembayaran akhir
def cetak_nota(total_kotor, total_diskon):
    print("\n======= NOTA PEMBAYARAN =======")
    print(f"Total Kotor  : Rp{total_kotor:,.0f}")
    print(f"Total Diskon : Rp{total_diskon:,.0f}")
    print(f"Total Bersih : Rp{total_kotor - total_diskon:,.0f}")
    print("================================")
    print("Terima kasih telah berbelanja di Toko Daging Wahyu Kenyot!")


#Program Utama
menu      = muat_menu()
pricelist = menu["pricelist"]
diskon_db = menu["diskon"]

total_kotor  = 0
total_diskon = 0

print("=== KASIR TOKO DAGING ===")
print("Ketik 'cukup' untuk selesai.\n")

while True:
    daging = input("Jenis daging yang ingin dibeli (Ayam/Sapi/Babi): ").capitalize()

    if daging == "Cukup":
        break

    if daging not in pricelist:
        print("Daging tidak tersedia!\n")
        continue

    kg       = float(input(f"Jumlah kg {daging}: "))
    subtotal = pricelist[daging] * kg
    diskon   = hitung_diskon(daging, kg, subtotal, diskon_db)

    total_kotor  += subtotal
    total_diskon += diskon
    print(f"  Subtotal: Rp{subtotal:,.0f} | Diskon: Rp{diskon:,.0f}\n")

cetak_nota(total_kotor, total_diskon)