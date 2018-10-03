FROM python:3.7
LABEL maintainer=corydominguez@gmail.com

COPY requirements.txt /
RUN pip install -r /requirements.txt
