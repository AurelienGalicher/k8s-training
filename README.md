# k8s-training

## Objectives
This small project is a "discovery tour" of k8s (kubernetes).
Using kubernetes and docker, we will set up a small streaming infrastructure that will take in input a flow of timeseries datapoints and output predictions based on machine learning models trained on the collected data.
the architecture involves:
<li> a kafka pub-sub cluster </li>
<li> an elasticsearch-logstah-kibana cluster (to visualize kafka streams) </li>
<li> a mongodb cluster (to store datapoints adn provide training) </li>
<li> a webservice build on top of flask (REST-API to our ml algorithm)</li>
<li> various connectors to stream data between the various components </li>
##

we first create storage 
```shell
kubectl create -f google-storage/
```

```shell
kubectl create -f zookeeper/
kubectl create -f kafka/
kubectl create -f mongo/
kubectl create -f elk/
kubectl create -f ts-simulator/

```
