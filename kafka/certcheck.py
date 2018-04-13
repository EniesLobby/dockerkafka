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

	try:
		con = KafkaConsumer(bootstrap_servers="localhost:9092")
	except:
		print("No Brokers Available")
		exit()
	
	con.assign([TopicPartition('certs', 0)])
	con.seek_to_beginning()
	print("Topics: ", con.topics())
	
	for msg in con:		
		current_time = str(datetime.datetime.now())	
		data = json.loads(msg.value.decode('utf-8'))		
		
		##CSRF####
		client = requests.session()
		client.get(url)
		
		if 'csrftoken' in client.cookies:
			csrftoken = client.cookies['csrftoken']
		##########
		
		payload = {'serial': data['serial'], 'csrfmiddlewaretoken': csrftoken }
		r = client.post(url, data=payload, headers={'Referer': url})
		if(r.text == ""):
			print(current_time, data['commonName'], "[x] NOT FOUND (!!!)")
		else:
			print(current_time, data['commonName'], "[x] FOUND")
				


if __name__ == "__main__":
	
	argparser = argparse.ArgumentParser(prog='certcheck')
	argparser.add_argument('--dbhost', help='hostname', default='localhost')
	argparser.add_argument('--dbuser', help='db user', default='postgres')
	argparser.add_argument('--dbname', help='db name', default='certwatch')
	argparser.add_argument('--port', help='db port', default='5433')
	args = argparser.parse_args()
	
	
	main(args)
	#test()
