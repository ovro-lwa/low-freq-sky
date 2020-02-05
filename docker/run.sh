#!/bin/bash

if [ ! -f /low-freq-sky/.secret_done ]; then
	key=$(dd if=/dev/urandom bs=50 count=1 | base64)
	echo "SECRET_KEY = '${key}'" >> /low-freq-sky/app/LowFreqSky/settings.py && touch /low-freq-sky/.secret_done
fi

nginx
uwsgi /low-freq-sky/uwsgi_low-freq-sky.ini
