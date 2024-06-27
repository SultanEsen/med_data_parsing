FROM python:3.10-alpine

WORKDIR /data_parsers

COPY ../requirements.txt /data_parsers/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /data_parsers/requirements.txt

COPY ./src /data_parsers

# EXPOSE 8080

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99