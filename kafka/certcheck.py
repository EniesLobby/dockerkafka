from kafka import KafkaConsumer, KafkaProducer
from kafka import TopicPartition
import json
import psycopg2
import sys
import datetime
import argparse
import base64
import requests

def main(args):
	
	url = "https://www.ct-observatory.org/checkcertserial"
	
	##CSRF####
	client = requests.session()
	client.get(url)
	
	if 'csrftoken' in client.cookies:
		csrftoken = client.cookies['csrftoken']
		print(csrftoken)
	##########
	
	payload = {'serial': 'FAFA52525252FF22', 'csrfmiddlewaretoken': csrftoken }
	
	#r = requests.post(url, payload, headers={'Referer': 'www.yandex.ru'})
	r = client.post(url, data=payload, headers={'Referer': url})
	
	print(r.text)
	
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
