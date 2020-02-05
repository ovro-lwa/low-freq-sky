FROM debian:buster
RUN apt-get update -y
RUN apt-get dist-upgrade -y
RUN apt-get install -y python3-django python3-casacore nginx uwsgi uwsgi-plugin-python3
RUN ln -s /usr/share/casacore/data/ephemerides/DE200 /var/lib/casacore/data/ephemerides
RUN ln -s /usr/share/casacore/data/ephemerides/DE405 /var/lib/casacore/data/ephemerides
COPY low-freq-sky /low-freq-sky
COPY docker/nginx_conf /etc/nginx/sites-available/default
COPY docker/uwsgi_low-freq-sky.ini /low-freq-sky
COPY docker/run.sh /low-freq-sky
EXPOSE 80
CMD ["/low-freq-sky/run.sh"]
