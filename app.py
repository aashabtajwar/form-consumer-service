import queue
import pika 


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare('atlan_task')
    channel.basic_consume(queue='atlan_task', auto_ack=True, on_message_callback=callback)
    channel.start_consuming()



if __name__ == '__main__':
    main()