# file: main.py

from message_server import MessageBroker, Subscriber, MessageServer

def fibo(n):
    if n <= 1:
        return n
    return fibo(n-1) + fibo(n-2)

if __name__ == "__main__":
    broker = MessageBroker()

    # esempio di subscriber
    user_service = Subscriber("user-service")
    log_service = Subscriber("log-service")

    broker.subscribe("user.created", user_service)
    broker.subscribe("user.created", log_service)

    user_service.handle = lambda message:print(f"{fibo(10)}") # sovrascrivo il metodo handle del subscriber per testare la CPU
    
    
    server = MessageServer(host="0.0.0.0", port=2604, broker=broker)
    server.start()
