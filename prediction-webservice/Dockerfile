FROM python:alpine
MAINTAINER galicher@gmail.com

# Install mongo
RUN pip install pymongo
RUN pip install pandas

# Install flaskapp
COPY src /flaskapp
RUN pip install -e /flaskapp

ENV FLASK_APP=flaskr
EXPOSE 5000

# Entrypoint
ENTRYPOINT ["flask", "run"]

