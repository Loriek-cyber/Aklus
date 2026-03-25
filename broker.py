from message_server import MessageBroker, Subscriber

if __name__ == "__main__":
    broker = MessageBroker()

    # esempio di subscriber
    messaggio_service = Subscriber("messaggio-service")
    broker.subscribe("messaggio.created", messaggio_service)
    