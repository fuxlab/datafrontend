FROM python:3.6.4

RUN apt-get update
RUN apt-get install pylint curl --assume-yes

ENV PYTHONUNBUFFERED 1


# install node js
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y nodejs

RUN npm install -g create-react-app
RUN npm install webpack-bundle-tracker
RUN npm install -g react-router-dom

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY startup.sh /usr/local/startup.sh