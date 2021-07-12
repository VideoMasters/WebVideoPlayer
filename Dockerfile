FROM tiangolo/uwsgi-nginx-flask:flask

# copy over our requirements.txt file
COPY requirements.txt /tmp/

# upgrade pip and install required python packages
RUN pip3 install -U pip
RUN pip3 install -r /tmp/requirements.txt

# copy over our app code
COPY ./app /app

ENV MESSAGE "Starting app"
