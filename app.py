import queue
import pika 
import json

from sheets import UpdateSheet
from extension import logging

def callback(ch, method, properties, body):
    logging.info('Dequeued data from queue')
    # consume the data
    # upload data to sheets
    # the data should be in the form [['a', 'b', 'c' ]]
    print(body)
    # log -> dequeued data, now processing for upload
    data = json.loads(body)
    form_id = data['form_id']
    form_link = data['link']
    sheet_name = data['sheet_name']
    update_sheet = UpdateSheet()
    update_sheet.upload_data(data['data'], form_id, form_link, sheet_name)
    # print(data)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare('atlan_task')
    channel.basic_consume(queue='atlan_task', auto_ack=True, on_message_callback=callback)
    channel.start_consuming()



if __name__ == '__main__':
    main()


# note : 
# Works with server!