import socket

HOST = "127.0.0.1"
PORT = 65432

binary_file = b""
with open("session-3/error_log.txt", "rb") as f:
    binary_file = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Sending binary file of size {len(binary_file)} bytes")
    s.sendall(binary_file)
    data = s.recv(1024)
    print(f"Received: {data.decode()}")
