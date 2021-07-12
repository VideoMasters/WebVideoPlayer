FROM tiangolo/uwsgi-nginx-flask:python3.8

LABEL maintainer="Deshdeepak <rkdeshdeepak1@gmail.com>"

ENV LISTEN_PORT 443
EXPOSE 443

# copy over our requirements.txt file
COPY requirements.txt /tmp/

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

# copy over our app code
COPY ./app /app

ENV MESSAGE "Starting app"
