#FROM python:3
FROM gcr.io/my-ml-prod-env/ts-simulator:latest
MAINTAINER galicher@gmail.com

# copy app src
ADD src/model_training.py /python_app/app.py

# Install requirements
#RUN apt-get update
#RUN apt-get install -y libblas-dev liblapack-dev liblapacke-dev gfortran
#RUN pip install --upgrade pip
#RUN pip install numpy
#RUN pip install scipy
#RUN pip install -U scikit-learn
#RUN pip install pymongo
#RUN pip install kafka-python
#RUN pip install requests


# Entrypoint
ENTRYPOINT ["python", "/python_app/app.py"]

