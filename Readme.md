# low-freq-sky

Web app to show what's in the sky at any date/time.
Preseeded with low frequency (100 MHz) objects but
any objects can be added.

## Quickstart

`docker run -d -p 8081:80 sabourke/low-freq-sky`

Then go to [localhost:8081](http://localhost:8081/)

`8081` can be replaced with any port you want to run the service on.

On a server use:

`docker run -d -p 8081:80 --restart unless-stopped sabourke/low-freq-sky`

to have it started automatically when docker daemon starts.

## Add new objects

Objects can be added through the admin interface at
[localhost:8081/admin](http://localhost:8081/admin/):
```
username: admin
password: lowfreqsky (CHANGE THIS)
```
or in Python in the container: `python3 manage.py shell`
see `init_sources.py` for examples.


