# PubMed-challenge-server

# PubMed Flask Server
Requirements: Python 3.5+ along with pip (https://www.python.org/downloads/)

#### Setup

Install virtualenv:
```
$ pip install virtualenv
```

Build a new virtualenv:
```
$ virtualenv .venv
```

Run Virtual env:
```
$ source ./.venv/bin/activate
```

Install dependencies:
```
$ pip install -r requirements.txt
```

<br>

#### Start server

##### For development purposes use:
```
(.venv) $ python app.py
```

##### For production environment use:
```
(.venv) $ gunicorn --bind 0.0.0.0:8080 wsgi
```

A Flask server will start at http://localhost:8080. 

To stop the server, press Ctrl+C.


To deactivate virtualenv:
```
(.venv) $ deactivate # deactivate the virtualenv
```
<br>

- To host this API on cloud instance, follow this step by step procedure: https://pyliaorachel.github.io/blog/tech/system/2017/07/07/flask-app-with-gunicorn-on-nginx-server-upon-aws-ec2-linux.html