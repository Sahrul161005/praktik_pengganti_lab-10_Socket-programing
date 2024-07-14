# echoserver.py

import socket
import threading

HOST = "192.168.1.18"  #alamat ip untuk server
PORT = 65432  # Port yang digunakan untuk berkomunikasi dengan server

clients = []  # Daftar untuk menyimpan klien yang terhubung

#pembuatan broadcast
def broadcast(message, sender_conn):
    """Kirim pesan ke semua klien kecuali pengirim"""
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message.encode("utf-8"))
            except:
                clients.remove(client)


def handle_client(conn, addr):
    print(f"Connected by {addr}")

    # Terima username dari client
    username = conn.recv(1024).decode("utf-8").strip()
    welcome_message = f"Welcome, {username}!"
    conn.sendall(welcome_message.encode("utf-8"))

    clients.append(conn)  # Tambahkan koneksi ke daftar klien yang terhubung

    try:
        while True:
            message = conn.recv(1024).decode("utf-8").strip()
            if not message:
                break
            response = f"{username}: {message}"
            print(response)  # Cetak pesan di server
            broadcast(response, conn)  # Broadcast pesan ke semua klien
    except ConnectionResetError:
        print(f"Connection with {addr} closed forcibly")
    finally:
        print(f"Disconnected from {addr}")
        clients.remove(conn)  # Hapus koneksi dari daftar klien
        conn.close()


# Main program
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server is listening...")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
