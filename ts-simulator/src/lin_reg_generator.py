from __future__ import print_function

from kafka import KafkaProducer
from sklearn.datasets.samples_generator import make_regression
import json
import time
import datetime
import sys

  
def generate_record(X, y, i, feat_names, target_name):
  data = dict(zip(feat_names,X[i,:].ravel().tolist()))
  timestp = datetime.datetime.now().isoformat()
  data.update({'timestamp':timestp})
  target = { 'target':y.ravel()[i]}
  #data.update(target)
  target.update({'timestamp':timestp})
  return data, target
  
def send_record(client, topic_str, X, y, i, feat_names, target_name):
  data, target = generate_record(X, y, i, feat_names, target_name)
  client.send(topic=topic_str,value=json.dumps(data).encode(encoding='UTF-8'),key=b'features')
  client.send(topic=topic_str,value=json.dumps(target).encode(encoding='UTF-8'),key=b'target')
  return data, target

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: lin_reg_generator.py <kafka_connection_string> <topic>", file=sys.stderr)
        sys.exit(-1)
    
    n_features = 10
    noise=0.1
    N = 60*10
    #data_topic_str = 'lin_reg_data'
    #target_topic_str = 'lin_reg_target'
    kafka_str, topic_str = sys.argv[1:]
    print (kafka_str)
    print (topic_str)
    
    try:
      client = KafkaProducer(bootstrap_servers=kafka_str)#"kafka:9092")
      #data_topic = client.topics[str.encode(data_topic_str)]
      #target_topic = client.topics[str.encode(target_topic_str)]
      #data_producer = data_topic.get_producer()
      #target_producer = target_topic.get_producer()
      feat_names = ['feat_%s' % (i) for i in range(n_features)]
      target_name =['target']
      while True:
        X, y = make_regression(n_samples=N,n_features=n_features,noise=noise)
        for i in range(N):
          data, target = send_record(client, topic_str, X, y, i, feat_names, target_name)
          print (data)
          print (target)
          time.sleep(1)

    except:
      print ("connection failed")

    

