import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))

def handle_client(conn, addr):
    connected = True
    while connected:
        filename = conn.recv(2048)
        print(filename.decode())
        with open(filename, "wb") as f:
            while True:
                f.write(conn.recv(100000))

    conn.close()

def listen():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

listen()
