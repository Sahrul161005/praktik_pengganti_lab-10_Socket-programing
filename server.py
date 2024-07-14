# server-echo.py

import socket
import threading
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def handle_client(msg):
    conn, addr = msg
    print(f"Connected by {addr}")

    with conn:
        while True:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            data = f"Hi, {data}"
            conn.sendall(data.encode("utf-8"))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("Server is listening...")

    while True:
        # conn, addr = s.accept()
        # print(f"conn: {conn}")
        mesg = s.accept()
        thread = threading.Thread(target=handle_client, args={mesg})
        thread.start()

