#FROM python:3
FROM mykafkaconnectregistry.azurecr.io/ts-simulator:0
#gcr.io/my-ml-prod-env/ts-simulator:latest
MAINTAINER galicher@gmail.com

# Install mongo
#RUN apt-get update
#RUN apt-get install -y libblas-dev liblapack-dev liblapacke-dev gfortran
#RUN pip install --upgrade pip
#RUN pip install pymongo
RUN pip install pandas

# Install flaskapp
COPY src /flaskapp
RUN pip install -e /flaskapp

ENV FLASK_APP=flaskr
EXPOSE 5000

# Entrypoint
ENTRYPOINT ["flask", "run"]

