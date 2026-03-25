# file: test_client.py

import socket
import json

HOST = "10.87.34.207"
PORT = 2604

msg = {
    "topic": "user.created",
    "payload": {"user_id": 123, "name": "Arjel"}
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(json.dumps(msg).encode("utf-8"))
    data = s.recv(4096)

print("Risposta dal server:", data.decode("utf-8"))
