FROM python:3.7-slim-stretch
LABEL maintainer=corydominguez@gmail.com

RUN apt update && \
	apt upgrade -y && \
	apt install -y \
	gcc

COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN python3 -m spacy download en
