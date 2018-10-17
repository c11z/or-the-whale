FROM python:3.7-slim-stretch
LABEL maintainer=corydominguez@gmail.com

COPY requirements.txt /
COPY scripts/nltk_download.py /
RUN pip install -r /requirements.txt
RUN python3 nltk_download.py
