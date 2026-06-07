import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                with open("session-3/received_error_log.txt", "ab") as f:
                    f.write(data)
                if not data:
                    break
                print(f"Received: {data.decode()}")
                conn.sendall(data)
