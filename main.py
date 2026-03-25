# file: main.py

from message_server import MessageBroker, Subscriber, MessageServer

if __name__ == "__main__":
    broker = MessageBroker()

    # esempio di subscriber
    user_service = Subscriber("user-service")
    log_service = Subscriber("log-service")

    broker.subscribe("user.created", user_service)
    broker.subscribe("user.created", log_service)

    user_service.handle = lambda message: print(f"[user-service] Nuovo utente creato: {message.payload}")
    
    
    server = MessageServer(host="0.0.0.0", port=2604, broker=broker)
    server.start()
