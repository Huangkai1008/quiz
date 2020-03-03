FROM python:3.7.6-slim-stretch
LABEL maintainer="huangkai"

WORKDIR app
COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple