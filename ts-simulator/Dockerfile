FROM python:3
MAINTAINER galicher@gmail.com

# copy app src
ADD src/lin_reg_generator.py /python_app/app.py

# Install requirements
RUN apt-get update
RUN apt-get install -y libblas-dev liblapack-dev liblapacke-dev gfortran
RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install scipy
RUN pip install -U scikit-learn
RUN pip install pymongo
RUN pip install kafka-python



# Entrypoint
ENTRYPOINT ["python", "/python_app/app.py"]

