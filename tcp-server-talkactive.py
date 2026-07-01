import socket
import threading

HOST = 'localhost'
PORT = 8001

# Kata perintah untuk memutus koneksi (boleh diketik oleh server maupun client)
PERINTAH_PUTUS = {'exit', 'quit', 'putus'}

def terima_pesan(conn, stop_event):
    """Berjalan di thread terpisah: TERUS menerima & menampilkan pesan dari client,
    supaya server tetap bisa mengetik balasan kapan saja tanpa terblokir."""
    while not stop_event.is_set():
        try:
            data = conn.recv(1024)
        except OSError:
            break
        if not data:
            print("\n[Client memutuskan koneksi. Tekan Enter untuk keluar.]")
            stop_event.set()
            break
        pesan = data.decode('utf-8')
        if pesan.strip().lower() in PERINTAH_PUTUS:
            print("\n[Client meminta putus koneksi. Tekan Enter untuk keluar.]")
            stop_event.set()
            break
        # Tampilkan pesan masuk, lalu cetak ulang prompt agar rapi
        print(f"\nClient : {pesan}")
        print("Anda (server): ", end="", flush=True)

def start_chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Supaya port bisa langsung dipakai lagi tanpa menunggu (hindari "Address already in use")
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server chat aktif di {HOST}:{PORT}, menunggu koneksi...")
    print("(Buka TERMINAL LAIN, lalu jalankan tcp-client-talkactive.py untuk menyambung)")

    # Menunggu client. Jika ditekan Ctrl+C saat menunggu, keluar dengan pesan rapi.
    try:
        conn, addr = server_socket.accept()
    except KeyboardInterrupt:
        print("\nServer dihentikan sebelum ada client menyambung.")
        server_socket.close()
        return

    print(f"Terhubung dengan client: {addr}")
    print(f"Ketik pesan lalu tekan Enter untuk mengirim. Ketik {PERINTAH_PUTUS} untuk memutus.\n")

    # Thread khusus penerima -> server bisa mengetik KAPAN SAJA tanpa menunggu client
    stop_event = threading.Event()
    penerima = threading.Thread(target=terima_pesan, args=(conn, stop_event), daemon=True)
    penerima.start()

    # Loop utama: server mengetik & mengirim pesan kapan saja
    try:
        while not stop_event.is_set():
            try:
                pesan = input("Anda (server): ")
            except EOFError:
                break
            if stop_event.is_set():
                break
            conn.sendall(pesan.encode('utf-8'))
            # Jika server yang mengetik perintah putus -> hentikan
            if pesan.strip().lower() in PERINTAH_PUTUS:
                print("\nAnda memutuskan koneksi. Menutup...")
                break
    except (KeyboardInterrupt, BrokenPipeError, ConnectionResetError):
        print("\nKoneksi terputus.")
    finally:
        stop_event.set()
        conn.close()
        server_socket.close()
        print("Koneksi selesai.")

if __name__ == "__main__":
    start_chat_server()
