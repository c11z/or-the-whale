FROM python:3.7-slim-stretch
LABEL maintainer=corydominguez@gmail.com

RUN apt update && \
	apt upgrade -y && \
	apt install -y \
	build-essential \
	cmake \
	gcc \
	protobuf-compiler \
	libprotoc-dev

COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN python3 -m spacy download en
RUN python3 -m spacy download en_core_web_lg
