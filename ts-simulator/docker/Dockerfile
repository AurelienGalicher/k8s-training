FROM python:alpine
MAINTAINER galicher@gmail.com

# Install mongo
RUN pip install pymongo
RUN pip install kafka-python
RUN pip install numpy
RUN pip install scipy
RUN pip install -U scikit-learn

# Install flaskapp
ADD ../src/lin_reg_generator.py /python_app/app.py

# Entrypoint
ENTRYPOINT ["ipython", "/python_app/app.py"]

