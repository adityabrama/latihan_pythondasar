import socket
import threading

HOST = 'localhost'
PORT = 8001

# Kata perintah untuk memutus koneksi (boleh diketik oleh client maupun server)
PERINTAH_PUTUS = {'exit', 'quit', 'putus'}

def terima_pesan(sock, stop_event):
    """Berjalan di thread terpisah: TERUS menerima & menampilkan pesan dari server,
    supaya client tetap bisa mengetik kapan saja tanpa terblokir."""
    while not stop_event.is_set():
        try:
            data = sock.recv(1024)
        except OSError:
            break
        if not data:
            print("\n[Server memutuskan koneksi. Tekan Enter untuk keluar.]")
            stop_event.set()
            break
        pesan = data.decode('utf-8')
        if pesan.strip().lower() in PERINTAH_PUTUS:
            print("\n[Server meminta putus koneksi. Tekan Enter untuk keluar.]")
            stop_event.set()
            break
        # Tampilkan pesan masuk, lalu cetak ulang prompt agar rapi
        print(f"\nServer : {pesan}")
        print("Anda (client): ", end="", flush=True)

def start_chat_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Coba sambung ke server. Jika server belum jalan, beri pesan yang jelas.
    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"Gagal menyambung ke {HOST}:{PORT}.")
        print("Pastikan tcp-server-talkactive.py sudah JALAN lebih dulu di terminal lain.")
        client_socket.close()
        return

    print(f"Terhubung ke server {HOST}:{PORT}")
    print(f"Ketik pesan lalu tekan Enter untuk mengirim. Ketik {PERINTAH_PUTUS} untuk memutus.\n")

    # Thread khusus penerima -> client bisa mengetik KAPAN SAJA tanpa menunggu server
    stop_event = threading.Event()
    penerima = threading.Thread(target=terima_pesan, args=(client_socket, stop_event), daemon=True)
    penerima.start()

    # Loop utama: client mengetik & mengirim pesan kapan saja
    try:
        while not stop_event.is_set():
            try:
                pesan = input("Anda (client): ")
            except EOFError:
                break
            if stop_event.is_set():
                break
            client_socket.sendall(pesan.encode('utf-8'))
            # Jika client yang mengetik perintah putus -> hentikan
            if pesan.strip().lower() in PERINTAH_PUTUS:
                print("\nAnda memutuskan koneksi. Menutup...")
                break
    except (KeyboardInterrupt, BrokenPipeError, ConnectionResetError):
        print("\nKoneksi terputus.")
    finally:
        stop_event.set()
        client_socket.close()
        print("Koneksi selesai.")

if __name__ == "__main__":
    start_chat_client()
