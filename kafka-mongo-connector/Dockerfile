FROM python:3
MAINTAINER galicher@gmail.com

# copy app src
ADD src/kafka-mongo-connector.py /python_app/app.py

# Install requirements
RUN pip install pymongo
RUN pip install kafka-python
RUN pip install python-dateutil



# Entrypoint
ENTRYPOINT ["ipython", "/python_app/app.py"]

