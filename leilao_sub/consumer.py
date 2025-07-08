import pika
import threading

class RabbitmqConsumer:
    def __init__(self, callback) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = "data_exchange"
        self.__callback = callback
        self.__connection = None
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(self.__username, self.__password)
        )

        self.__connection = pika.BlockingConnection(connection_parameters)
        channel = self.__connection.channel()

        channel.exchange_declare(exchange=self.__exchange, exchange_type='fanout', durable=True)

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=self.__exchange, queue=queue_name)

        channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=self.__callback)

        return channel

    def send_message(self, message: str):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(self.__username, self.__password)
        ))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.__exchange, exchange_type='fanout', durable=True)
        channel.basic_publish(
            exchange=self.__exchange,
            routing_key='',
            body=message.encode(),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()

    def start(self):
        print("Consumidor iniciado, aguardando itens...")
        self.__channel.start_consuming()

    def close(self):
        if self.__connection and self.__connection.is_open:
            self.__connection.close()


def callback_test(ch, method, properties, body):
    print(f"\n Mensagem recebida: {body.decode()}")
    print(" Envie seu lance: ", end='', flush=True)


if __name__ == "__main__":
    nome = input("👤 Digite seu nome: ")
    consumer = RabbitmqConsumer(callback_test)

    threading.Thread(target=consumer.start, daemon=True).start()

    try:
        while True:
            msg = input(" Envie seu lance: ")
            consumer.send_message(f"{nome}-> {msg}")
    except KeyboardInterrupt:
        consumer.close()
        print("\n Encerrado.")
