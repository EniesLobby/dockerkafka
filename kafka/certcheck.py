from kafka import KafkaConsumer, KafkaProducer
from kafka import TopicPartition
import json
import psycopg2
import sys
import datetime
import argparse
import base64


def connectToDatabase(name, port, user, host):
	try:
		db = psycopg2.connect(dbname=name, port=port, user=user, host=host)
		return db
	
	except:
		print("Error connecting to local database")
		exit()
		


def main(args):
	try:
	    db = connectToDatabase('certwatch', 5432, 'postgres', '172.19.0.2')
	except:
	    print("DATABASE CONNECTION ERROR")
	    exit()

	cursor = db.cursor()
	
	print("Connection to db established")
	
	try:
		con = KafkaConsumer(bootstrap_servers="localhost:9092")
	except:
		print("No Brokers Available")
	
	con.assign([TopicPartition('certs', 0)])
	con.seek_to_beginning()
	print("Topics: ", con.topics())
	
	key = 'serial'
	

	for msg in con:
		current_time = str(datetime.datetime.now())	
		data = json.loads(msg.value.decode('utf-8'))
		
		sqlQuery = """SELECT id FROM certificate WHERE serial=%s"""
		sqlQuery_commonName = """SELECT * FROM ca WHERE """
		
		if(key in data):
			serial_int = int(data[key], 16)
			serial = serial_int.to_bytes((serial_int.bit_length() + 15) // 8, 'big', signed=True) or b'\0'
			
			sqlData = (psycopg2.Binary(serial),)
			cursor.execute(sqlQuery, sqlData)
			result = cursor.fetchone()
			
			if (result != None):
				print('commonName: ', data['commonName'], current_time, 'serial original: ', data[key], 'serial byted: ', serial, 'serial in dec: ', serial_int, 'status: ', result)
			else:
				print('commonName: ', data['commonName'], current_time, 'serial original: ', data[key], 'serial byted: ', serial, 'serial in dec: ', serial_int, 'status: ', 'not found(!!!)')
				
				
		data = {}

	
########################## Testing ####
def test():
	
	try:
	    db = connectToDatabase('certwatch', 5433, 'postgres', 'localhost')
	except:
	    print("DATABASE CONNECTION ERROR")
	    exit()

	cursor = db.cursor()

	dec = 130458685923941780062625206130337997753
	hhex = "4708AB20C26C13AD4238AE6E92300655"
		
	hhex_dec = int(hhex, 15)
	print("hhex_dec = ", hhex_dec)
	
	print("ae = ", base64.b64decode(hhex))
	
	#cert = crypto.load_certificate(crypto.FILETYPE_ASN1, bytes(row[1]))
	
	dec_b = dec.to_bytes((dec.bit_length() + 15) // 8, 'big', signed=True) or b'\0'
	
	sqlQuery = """SELECT id FROM certificate WHERE serial=%s"""
	sqlData = (psycopg2.Binary(dec_b),)
	cursor.execute(sqlQuery, sqlData)
	result = cursor.fetchone()
	
	print("result = ", result)
	
	print("dec_b = ", dec_b)
#######################################		


if __name__ == "__main__":
	
	argparser = argparse.ArgumentParser(prog='certcheck')
	argparser.add_argument('--dbhost', help='hostname', default='localhost')
	argparser.add_argument('--dbuser', help='db user', default='postgres')
	argparser.add_argument('--dbname', help='db name', default='certwatch')
	argparser.add_argument('--port', help='db port', default='5433')
	args = argparser.parse_args()
	
	
	main(args)
	#test()
#Example of cert log
"""
{"ts":1514343803.87296,"id":"FZXuLft378cBVBYmh","certificate.version":3,
"certificate.serial":"1687D6886DE2300685233DBF11BF6597","certificate.subject":"CN=thawte SSL CA - G2,O=thawte\u005c, Inc.,C=US","certificate.issuer":"CN=thawte Primary Root CA,OU=(c) 2006 thawte\u005c, Inc. - For authorized use only,OU=Certification Services Division,O=thawte\u005c, Inc.,C=US","certificate.not_valid_before":1383202800.0,"certificate.not_valid_after":1698735599.0,
"certificate.key_alg":"rsaEncryption","certificate.sig_alg":"sha256WithRSAEncryption","certificate.key_type":"rsa",
"certificate.key_length":2048,"certificate.exponent":"65537","basic_constraints.ca":true,"basic_constraints.path_len":0}
"""


