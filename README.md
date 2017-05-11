# k8s-training

## Objectives
This small project is a "discovery tour" of k8s (kubernetes).
Using kubernetes and docker, we will set up a small streaming infrastructure that will take in input a flow of time serie's data points and output predictions based on machine learning models trained on the collected data.
the architecture involves:
<li> a kafka pub-sub cluster </li>
<li> an elasticsearch-logstah-kibana cluster (to visualize kafka streams) </li>
<li> a mongodb cluster (to store datapoints and provide training datasets) </li>
<li> a webservice build on top of flask (REST-API for our ml algorithm)</li>
<li> various connectors to stream data between the various components </li>

## Instructions

we first create storage class to dynamically provision storage on GCP 
```shell
kubectl create -f google-storage/
```
we then a kafka cluster (and a zookeeper cluster)
```shell
kubectl create -f zookeeper/
kubectl create -f kafka/
```
we then create a mongo cluster
```shell
kubectl create -f mongo/
```

we then create an elasticsearch cluster + and logstash and kibana instances
```shell
kubectl create -f elk/
kubectl create -f elk/logstash/
kubectl create -f elk/kibana/
```
we start generating "random timeseries" using a custom python script
```shell
kubectl create -f tssimulator/
```
