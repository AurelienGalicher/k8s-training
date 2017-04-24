from __future__ import print_function

from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
import json
import sys

  
# Load default config and override config from an environment variable

DATABASE_URL="mongodb://mongo:27017"
MONGO_REPLICASET="rs0"
DATABASE_NAME = 'mldb'
COLLECTION_NAME = 'ts'
DEBUG=True

KAFKA_BROKER = "kafka:9092"
TOPIC = "mltest"
WRITE_TOPIC = "mlscore"
GROUP_ID = "scorer"

def connect_db():
    """Connects to the specific database."""
    mongo = MongoClient(DATABASE_URL,replicaset=MONGO_REPLICASET)
    collection = mongo[DATABASE_NAME][COLLECTION_NAME]
    return collection

def connect_kafka():
    client = KafkaConsumer(TOPIC, group_id=GROUP_ID, bootstrap_servers=KAFKA_BROKER)
    writer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    return client, writer

def process_msg(msg, mongo_col, writer):
    data = json.loads(msg.value.decode('UTF-8'))
    key = msg.key.decode('UTF-8')
    print (key)
    try:
        timestamp = data['timestamp']
        if key == "prediction":
            res = mongo_col.find_one({"timestamp": timestamp})
            error = res['target'] - res['prediction']
            record = {'timestamp':timestamp, 
                                           'error':error,
                                          'ypred_':res['prediction'],
                                          'ytrue_':res['target']}
            writer.send(topic=WRITE_TOPIC,
                        value=json.dumps(record)\
                                  .encode(encoding='UTF-8'),key=b'error')
    except:
        record = "error no timestamp found in message"
    return record
        
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: kafka_mongo_connector <kafka_connection_string> <topic> <mongo_url> <replicaset>", file=sys.stderr)
        sys.exit(-1)
    
    KAFKA_BROKER, TOPIC, DATABASE_URL, MONGO_REPLICASET = sys.argv[1:]
    print (KAFKA_BROKER, TOPIC, DATABASE_URL, MONGO_REPLICASET)
    #print (topic_str)
    
    #try:
    client, writer = connect_kafka()
    mongo_col = connect_db()
    for msg in client:
        res = process_msg(msg, mongo_col, writer)
        print (res)
    #except:
    #    print ("error")
    #    pass
