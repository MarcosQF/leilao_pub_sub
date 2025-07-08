import pika

class RabbitmqConsumer:
    def __init__(self, callback) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = "data_exchange"
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(self.__username, self.__password)
        )

        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()

        channel.exchange_declare(exchange=self.__exchange, exchange_type='fanout', durable=True)

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=self.__exchange, queue=queue_name)

        channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=self.__callback)

        return channel

    def start(self):
        print("Consumidor iniciado, aguardando mensagens...")
        self.__channel.start_consuming()


def callback_test(ch, method, properties, body):
    print(f"Mensagem recebida: {body.decode()}")


if __name__ == "__main__":
    consumer = RabbitmqConsumer(callback_test)
    consumer.start()
