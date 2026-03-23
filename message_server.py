# file: message_server.py

class Message:
    def __init__(self, topic: str, payload: dict):
        self.topic = topic
        self.payload = payload


class Subscriber:
    def __init__(self, name: str):
        self.name = name

    def handle(self, message: Message):
        # qui decidi cosa succede quando ricevi un messaggio
        print(f"[{self.name}] ricevuto su {message.topic}: {message.payload}")


class MessageBroker:
    def __init__(self):
        # topic -> lista di Subscriber
        self.subscribers = {}

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
            # nessuno iscritto: per ora ignoro
            return
        for subscriber in self.subscribers[topic]:
            subscriber.handle(message)
