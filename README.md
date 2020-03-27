# OX rest API

Open-Xchange administration Rest API

Get Started:
```
cd ox-rest-api
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```

You will need to set the following env vars:

OXAPI_SECRET_KEY='SECRETKEY'
OXAPI_DB_URI='mysql://user:pass@localhost/database'
OXAPI_ENVIRONMENT='development' -> or production

OXAASADMHOST -> Open Xchange Hostname
OXAASADMNAME -> Open Xchange Admin User
OXAASADMPASS -> Open Xchange Admin Password



### Usage
You will need to initialize database if it is a new install and then create a new master user.

```sh
python oxapi.py db init
python oxapi.py db admin
```

Starting the server
```
python oxapi.py runserver
```

