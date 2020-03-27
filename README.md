# PubMed-challenge-server

## PubMed Flask Server

Key features:
- Uses NCBI's public APIs, specifically the PubMed database
- Automatic logging of requests
- Production ready environment with gunicorn

#### Setup

Requirements: Python 3.5+ along with pip (https://www.python.org/downloads/)

<br/>

Install virtualenv:
```
$ pip install virtualenv
```

Build a new virtualenv:
```
$ virtualenv .venv
```

Run virtualenv:
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
(.venv) $ deactivate 
```
<br>

- To host this API on cloud instance (AWS EC2 linux), follow this step by step procedure: https://pyliaorachel.github.io/blog/tech/system/2017/07/07/flask-app-with-gunicorn-on-nginx-server-upon-aws-ec2-linux.html
