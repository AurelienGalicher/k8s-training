from __future__ import print_function

from kafka import KafkaConsumer
from pymongo import MongoClient
import json
from dateutil import parser
import sys

  
# Load default config and override config from an environment variable

DATABASE_URL="mongodb://mongo:27017"
MONGO_REPLICASET="rs0"
DATABASE_NAME = 'mldb'
COLLECTION_NAME = 'ts'
DEBUG=True

KAFKA_BROKER = "kafka:9092"
TOPIC = "mltest"
GROUP_ID = "kafka_mongo_connector_consumer"

def connect_db():
    """Connects to the specific database."""
    mongo = MongoClient(DATABASE_URL,replicaset=MONGO_REPLICASET)
    #if COLLECTION_NAME in mongo[DATABASE_NAME].collection_names():
    collection = mongo[DATABASE_NAME][COLLECTION_NAME]
    #else:
    #    mongo[DATABASE_NAME].create_collection(COLLECTION_NAME)
    #    collection = mongo[DATABASE_NAME][COLLECTION_NAME]
    #    collection.createIndex( { "timestamp": 1 }, { 'unique': True } )
    return collection

def connect_kafka():
    client = KafkaConsumer(TOPIC, group_id=GROUP_ID, bootstrap_servers=KAFKA_BROKER)
    return client

def read_write_to_mongo(msg, mongo_col):
    data = json.loads(msg.value.decode('UTF-8'))
    try:
        timestamp = data['timestamp']
        data.update({'time': parser.parse(data['timestamp'])})
        res = mongo_col.update_one({'timestamp':timestamp},
                             {'$set':data }, upsert=True)
    except:
        res = "error no timestamp found in message"
    return res
        
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: kafka_mongo_connector <kafka_connection_string> <topic> <mongo_url> <replicaset>", file=sys.stderr)
        sys.exit(-1)
    
    KAFKA_BROKER, TOPIC, DATABASE_URL, MONGO_REPLICASET = sys.argv[1:]
    print (KAFKA_BROKER, TOPIC, DATABASE_URL, MONGO_REPLICASET)
    #print (topic_str)
    
    #try:
    client = connect_kafka()
    mongo_col = connect_db()
    for msg in client:
        res = read_write_to_mongo(msg, mongo_col)
        print (res)
    #except:
    #    print ("error")
    #    pass
