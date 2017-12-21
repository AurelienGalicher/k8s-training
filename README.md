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

## Functional architecture

![alt text](https://github.com/AurelienGalicher/k8s-training/raw/master/img/ArchiFuncML.png "")

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

we then create an elasticsearch cluster + logstash and kibana instances
```shell
kubectl create -f elk/
```

we start create topics in our kafka pub-sub queue
```shell
kubectl create -f kafka-topics/
```

we start sending "random timeseries" to our kafka queue using a custom python script
```shell
kubectl create -f ts-simulator/
```

we connect to our kafka queue to mongodb 
```shell
kubectl create -f kafka-mongo-connector/
```

we build a webservice to support our ml algorithm
```shell
kubectl create -f prediction-webservice/
```

we train our ml model on data collected on our mongo cluster
```shell
kubectl create -f training-job/
```
we connect our web-service to the kafka feed
```shell
kubectl create -f kafka-webapp-connector/
```

we now can connect to kibana to monitor our projects.
```shell
kubectl get svc kibana
```
get the public ip address of the kibana service and open our favorite browser.
You can for example monitor the average squared error over a timeframe of 30 seconds using timelion using this request:
```
.es(metric=avg:target).subtract(.es(metric=avg:prediction)).multiply(.es(metric=avg:target).subtract(.es(metric=avg:prediction))).movingaverage(30)
```

