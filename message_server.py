# file: message_server.py

import socket
import json
from typing import Dict


class Message:
    def __init__(self, topic: str, payload: dict):
        self.topic = topic
        self.payload = payload


class Subscriber:
    def __init__(self, name: str):
        self.name = name

    def handle(self, message: Message):
        print(f"[{self.name}] ricevuto su {message.topic}: {message.payload}")


class MessageBroker:
    def __init__(self):
        self.subscribers: Dict[str, list[Subscriber]] = {}

    def subscribe(self, topic: str, subscriber: Subscriber):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(subscriber)

    def unsubscribe(self, topic: str, subscriber: Subscriber):
        if topic in self.subscribers:
            self.subscribers[topic] = [
                s for s in self.subscribers[topic] if s is not subscriber
            ]

    def publish(self, topic: str, payload: dict):
        message = Message(topic, payload)
        if topic not in self.subscribers:
            return
        for subscriber in self.subscribers[topic]:
            subscriber.handle(message)


class MessageServer:
    def __init__(self, host: str, port: int, broker: MessageBroker):
        self.host = host
        self.port = port
        self.broker = broker

    def start(self):
        # server TCP base, bloccante, una connessione alla volta.[web:20][web:17]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"MessageServer in ascolto su {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                print(f"Connessione da {addr}")
                with conn:
                    data = conn.recv(4096)
                    if not data:
                        continue

                    try:
                        # mi aspetto qualcosa tipo:
                        # {"topic": "user.created", "payload": {"user_id": 123}}
                        msg_obj = json.loads(data.decode("utf-8"))
                        topic = msg_obj.get("topic")
                        payload = msg_obj.get("payload", {})

                        if topic:
                            self.broker.publish(topic, payload)
                            response = {"status": "ok"}
                        else:
                            response = {"status": "error", "error": "missing topic"}

                    except json.JSONDecodeError:
                        response = {"status": "error", "error": "invalid json"}

                    conn.sendall(json.dumps(response).encode("utf-8"))
