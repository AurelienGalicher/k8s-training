# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 18:09:33 2017

@author: J0230022
"""

from __future__ import print_function

from kafka import KafkaConsumer, KafkaProducer
import requests
from bson import json_util
import json
import sys

KAFKA_BROKER = "kafka:9092"
TOPIC = "mltest"
GROUP_ID = "kafka_predictions"

MODEL_NAME = "ridgecv"
VERSION = 0

PREDICTION_SERVICE = "http://prediction/predict/"

def connect_kafka():
    read_client = KafkaConsumer(TOPIC, group_id=GROUP_ID, bootstrap_servers=KAFKA_BROKER)
    write_client = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    return read_client, write_client

def predict(msg, write_client, model_name, version):
    if msg.key.decode('UTF-8') == 'features':
        data = json.loads(msg.value.decode('UTF-8'))
        
        #timestamp = data['timestamp']
        #feats = [ key for key in data.keys() if key.startswith('feat')]
        
        connection_url = PREDICTION_SERVICE+model_name+'/'+str(version)+'/'
        print (connection_url)
        r = requests.post(connection_url, {'data': json.dumps([data], default=json_util.default)})
        print (r.text)
        prediction = json.loads(r.text)
        for pred in prediction:
            #pred.update({'model':model_name,'version':version})
            write_client.send(topic=TOPIC,value=json.dumps(pred).encode(encoding='UTF-8'),key=b'prediction')
            print (pred)
    return

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: stream_predict.py <topic> <model_name> <version>", file=sys.stderr)
        sys.exit(-1)

    TOPIC, MODEL_NAME, VERSION= sys.argv[1:]

    read_client, write_client = connect_kafka()
    
    for msg in read_client:
        predict(msg, write_client, MODEL_NAME, VERSION)
