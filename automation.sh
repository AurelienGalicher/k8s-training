#!/bin/bash

#we first create storage class to dynamically provision storage on GCP
kubectl create -f google-storage/

#we then a kafka cluster (and a zookeeper cluster)
kubectl create -f zookeeper/
sleep 60
kubectl create -f kafka/
sleep 60
#we then create a mongo cluster
kubectl create -f mongo/
sleep 60
#we then create an elasticsearch cluster + and logstash and kibana instances
kubectl create -f elk/
sleep 60
#we start create topics in our kafka pub-sub queue
kubectl create -f kafka-topics/
sleep 60
#we start send "random timeseries" to our kafka queue using a custom python script
kubectl create -f ts-simulator/
sleep 20
#we connect to our kafka queue to mongodb
kubectl create -f kafka-mongo-connector/
sleep 60
#we build a webservice to support our ml algorithm
kubectl create -f prediction-webservice/
sleep 60
#we train our ml model on data collected on our mongo cluster
kubectl create -f training-job/
sleep 60
#we connect our web-service to the kafka feed

kubectl create -f kafka-webapp-connector/
