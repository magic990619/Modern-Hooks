FROM mediasapiens/python3
WORKDIR /web

COPY requirements.txt /requirements.txt

RUN apt-get update
RUN apt-get -y install gunicorn
