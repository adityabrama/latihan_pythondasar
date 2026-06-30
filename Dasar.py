#Trial Program
#nama_program = "Belajar Python"
#versi = 1
#print(f"---Selamat Datang di {nama_program} v{versi}---")

#Trial Nama
#nama_user = input ("Masukkan nama Anda: ")
#usia = int(input("Masukkan usia Anda:"))

#print(f"Halo {nama_user}, tahun depan usia Anda adalah {usia+1} tahun.")

#TRY CASES

#harga_daging_ayam_1_kilo = 20000
#jumlah_transaksi = 0
#grand_total = 0

#Buat pertanyaan sistem terkait pembelian bisa lebih dari 1x, sampai anda menginputkan "cukup"
#while True:
#    kg_input = input("Berapa Kg yang ingin dibeli? (ketik 'cukup' untuk berhenti) ")
#
 #   if kg_input == "cukup":
  #      print("\n--- Terima kasih telah berbelanja! ---")
   #     print(f"Total transaksi: {jumlah_transaksi}x pembelian")
    #    print(f"Total harga keseluruhan: {grand_total}")
     #   break
#
 #   kg = int(kg_input)
  #  harga_per_transaksi = harga_daging_ayam_1_kilo * kg
   # if 2 <= kg <= 5:
    #    diskon = 5000
     #   harga_setelah_diskon = harga_per_transaksi - diskon
      #  print(f"Anda mendapatkan Diskon sebesar {diskon}! Harga transaksi ini: {harga_setelah_diskon}")
   # elif kg > 5:
#        diskon = 7000
 #       harga_setelah_diskon = harga_per_transaksi - diskon
  #      print(f"Anda mendapatkan Diskon sebesar {diskon}! Harga transaksi ini: {harga_setelah_diskon}")
   # else:
    #    harga_setelah_diskon = harga_per_transaksi
     #   print("Tidak ada diskon")

    #jumlah_transaksi += 1
    #grand_total += harga_setelah_diskon


#PERCABANGAN
#total_belanja = 150000
#if total_belanja>= 200000
#elif

#PERULANGAN
#var_list = [1,2,3,4,5]
#for i in var_list:
#    print(i)

#ARRAY
#daftar_daging = ["ayam", "sapi", "babi"]

#print(f"Daging pertama: {daftar_daging[0]}")
#print(f"Daging ketiga: {daftar_daging[1]}")

#daftar_daging[2] = "kambing"
#print(f"Array setelah diubah: {daftar_daging}")

#daftar_daging.append("bebek")
#print(f"Array setelah ditambah: {daftar_daging}")

#DICTIONARY
#pricelist = {
#    "ayam": 20000,
#    "sapi": 100000,
#    "babi": 50000
#}

#print(f"Harga daging ayam: {pricelist['ayam']}")

#WHILE LOOP
#program_berjalan = True

#while program_berjalan:
#    print("--- MENU UTAMA ---" )
#    pilihan = input("Ketik 'keluar' untuk menutup program:").lower()
#
#    if pilihan == "keluar":
#        print("Sampai jumpa!")
#        program_berjalan = False



#Function
#Basic Function
def sapa_halo():
    print("Halo! Selamat belajar Python.")

sapa_halo()

#Parameter Function
def sapa_teman(nama):
    print(f"Halo {nama}, apa kabar?")

sapa_teman("Budi")
sapa_teman("Siti")

#Return Function
def mesin_pengolah(data):
    hasil = data * 2 #Proses rahasia
    return hasil    #Output

angka_asli = 10
hasil_akhir = mesin_pengolah(angka_asli)

print(f"Input: {angka_asli}, Output: {hasil_akhir}")


#JSON (JavaScript Object Notation)
#TASK: Wrap minimal 2 function, datanya diambil dari JSON
