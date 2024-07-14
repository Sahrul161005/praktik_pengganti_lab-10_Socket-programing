# NewClient.py

import socket
import threading

HOST = "127.0.0.1"  # Alamat IP atau hostname dari server
PORT = 65432  # Port yang digunakan oleh server


def receive_messages(s):
    """Fungsi untuk menerima pesan dari server"""
    while True:
        try:
            message = s.recv(1024).decode("utf-8")
            if not message:
                break
            print(message)
        except:
            break


def send_message(s, username):
    """Fungsi untuk mengirim pesan ke server"""
    while True:
        message = input()
        if message.lower() == 'exit':
            break
        full_message = f"{username}: {message}"
        s.sendall(full_message.encode("utf-8"))


# Main program
if __name__ == "__main__":
    username = input("Masukkan username: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Kirim username ke server
        s.sendall(username.encode("utf-8"))

        # Terima pesan selamat datang dari server
        welcome_message = s.recv(1024).decode("utf-8")
        print(welcome_message)

        # Buat thread untuk menerima pesan dari server
        thread = threading.Thread(target=receive_messages, args=(s,))
        thread.start()

        # Kirim pesan ke server
        send_message(s, username)
