FROM 	nginx/unit:1.24.0-python3.9

COPY 	requirements.txt /tmp/requirements.txt

RUN 	pip install -r /tmp/requirements.txt                               \
    	&& apt autoremove --purge -y                                              \
    	&& rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

COPY 	./config.json /docker-entrypoint.d/config.json
COPY 	./webapp /bcp
