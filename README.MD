# Quick start guide
1. Create the .env configuration file in `/src/.env`. Example test server configuration:
    ```
    SECRET_KEY='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    DEBUG=True
    ALLOWED_HOSTS=.localhost,127.0.0.1
    DATABASE_URL=sqlite:///db.sqlite3
    DATABASE_ENGINE='django.db.backends.postgresql'
    DATABASE_HOST='postgres'
    DATABASE_NAME='rijp'
    DATABASE_USER='admin'
    DATABASE_PASS='passwd'
    DATABASE_PORT=5432
    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    CACHE_BACKEND=django.core.cache.backends.db.DatabaseCache
    CACHE_LOCATION='cache'
    CACHE_TIME_SHORT=0
    CACHE_TIME_MEDIUM=0
    CACHE_TIME_LONG=0
    URL_BASE=''
    ```
    * SECRET_KEY should be a 50-characters long string of random characters from the following set: `abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)`
    * `CACHE_BACKEND` can be set to:
        * `django.core.cache.backends.memcached.MemcachedCache` with location `127.0.0.1:11211` (default for python-memcached) 
        * `django.core.cache.backends.filebased.FileBasedCache` with location e.g. `/data/sb_cache/`
        * `django.core.cache.backends.db.DatabaseCache` with location e.g. `sb_cache_table`
        * `django.core.cache.backends.dummy.DummyCache` can be used during development 
    * `CACHE_TIME_SHORT`, `CACHE_TIME_MEDIUM` and `CACHE_TIME_LONG` are timers (in seconds) used for cache validation assigned to pages depending on how often their content changes
    * `URL_BASE` allows adding a URL prefix to all Station Book URLs
1. Make sure SQLite is configured as the default database in `src/rijp/settings.py`
1. Create the virtual environment:
    ```
    $ python3 -m venv env
    ```
1. Activate the virtual environment:
    ```
    $ source env/bin/activate
    ```
1. Install the dependencies:
    ```
    $ pip install -r requirements.txt
    ```
1. Go to the root directory:
    ```
    $ cd stationbook/
    ```
1. Prepare the database migration and apply it:
    ```
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    ```
1. Create the super user:
    ```
    $ python3 manage.py createsuperuser
    ```
1. Load the fixtures into the database:
    ```
    $ python3 manage.py loaddata data.json
    ```
1. Create the cache table in the database
    ```
    $ python3 manage.py createcachetable
    ```
1. Run the test server:
    ```
    $ python3 manage.py runserver 0.0.0.0:8080
    ```