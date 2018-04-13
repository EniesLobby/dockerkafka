from kafka import KafkaConsumer, KafkaProducer
from kafka import TopicPartition
import json
import psycopg2
import sys
import datetime
import argparse
import base64
import pika, os


# Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://wpjjevki:f3XA0SBfcSjtmnNyTmtUYRdlwBKGc2WD@sheep.rmq.cloudamqp.com/wpjjevki')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='certs') # Declare a queue


def main(args):
	
	try:
		con = KafkaConsumer(bootstrap_servers="localhost:9092")
	except:
		print("No Brokers Available")
	
	con.assign([TopicPartition('certs', 0)])
	con.seek_to_beginning()
	print("Topics: ", con.topics())
	
	for msg in con:
		
		current_time = str(datetime.datetime.now())	
		data = json.loads(msg.value.decode('utf-8'))
		serial = data['serial'] + "-" + data['commonName']
		channel.basic_publish(exchange='', routing_key='certs', body=serial)
		print(current_time, " [x] cert sent")


if __name__ == "__main__":
	
	argparser = argparse.ArgumentParser(prog='certcheck')
	argparser.add_argument('--dbhost', help='hostname', default='localhost')
	argparser.add_argument('--dbuser', help='db user', default='postgres')
	argparser.add_argument('--dbname', help='db name', default='certwatch')
	argparser.add_argument('--port', help='db port', default='5433')
	args = argparser.parse_args()
	
	
	main(args)
	#test()
