#!/bin/bash

#we first create storage class to dynamically provision storage on GCP
kubectl create -f google-storage/

#we then a kafka cluster (and a zookeeper cluster)
kubectl create -f zookeeper/
kubectl create -f kafka/

#we then create a mongo cluster
kubectl create -f mongo/

#we then create an elasticsearch cluster + and logstash and kibana instances
kubectl create -f elk/

#we start create topics in our kafka pub-sub queue
kubectl create -f kafka-topics/

#we start send "random timeseries" to our kafka queue using a custom python script
kubectl create -f ts-simulator/

#we connect to our kafka queue to mongodb
kubectl create -f kafka-mongo-connector/

#we build a webservice to support our ml algorithm
kubectl create -f prediction-webservice/

#we train our ml model on data collected on our mongo cluster
kubectl create -f training-job/

#we connect our web-service to the kafka feed

kubectl create -f kafka-webapp-connector/
