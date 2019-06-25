FROM python:3.7.3

RUN apt-get update
RUN apt-get install pylint curl --assume-yes
RUN apt-get install libpq-dev --assume-yes

ENV PYTHONUNBUFFERED 1

# install node js
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y nodejs

# install yarn
RUN npm install -g yarn

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -U scikit-image
RUN pip install -U cython
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY startup.sh /usr/local/startup.sh