#FROM python:3
FROM gcr.io/my-ml-prod-env/ts-simulator:latest
MAINTAINER galicher@gmail.com

# copy app src
ADD src/kafka-mongo-connector.py /python_app/app.py

# Install requirements
#RUN pip install pymongo
#RUN pip install kafka-python
RUN pip install python-dateutil



# Entrypoint
ENTRYPOINT ["python", "/python_app/app.py"]

