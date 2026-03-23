# file: main.py

from message_server import MessageBroker, Subscriber

if __name__ == "__main__":
    broker = MessageBroker()

    user_service = Subscriber("user-service")
    log_service = Subscriber("log-service")

    broker.subscribe("user.created", user_service)
    broker.subscribe("user.created", log_service)

    broker.publish("user.created", {"user_id": 123, "name": "Arjel"})
    broker.publish("user.deleted", {"user_id": 123})
