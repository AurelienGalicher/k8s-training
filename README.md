# k8s-training

## Objectives
This small project is a "discovery tour" of k8s (kubernetes).
Using kubernetes and docker, we will set up a small streaming infrastructure that will take in input a flow of timeseries datapoints and output predictions based on machine learning models trained on the collected data.
the architecture involves:
<li> a kafka pub-sub cluster </li>
<li> an elasticsearch-logstah-kibana cluster (to visualize kafka streams) </li>
*item a mongodb cluster (to store datapoints adn provide training)
*item a webservice build on top of flask (REST-API to our ml algorithm)
*item various connectors to stream data between the various components
##
```shell

kubectl create -f google-storage/
kubectl create -f zookeeper/
kubectl create -f kafka/
kubectl create -f mongo/
kubectl create -f elk/
kubectl create -f ts-simulator/

```
