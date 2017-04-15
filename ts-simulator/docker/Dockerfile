FROM python:alpine
MAINTAINER galicher@gmail.com

# Install requirements
RUN apt-get update
RUN apt-get install -y libblas-dev liblapack-dev liblapacke-dev gfortran
RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install scipy
RUN pip install -U scikit-learn
RUN pip install pymongo
RUN pip install kafka-python

# Install app
ADD ../src/lin_reg_generator.py /python_app/app.py

# Entrypoint
ENTRYPOINT ["ipython", "/python_app/app.py"]

