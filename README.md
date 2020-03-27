# PubMed-challenge-server

# Flask Server
Requirements: Python 3.5+ along with pip (https://www.python.org/downloads/)

#### Install virtualenv
```
 $ pip install virtualenv
```
#### Run Virtual env
```
$ source ./.venv/bin/activate
```

#### For development purposes use:
```
(.venv) $ python app.py
```

#### For production environment use:
```
(.venv) $ gunicorn --bind 0.0.0.0:8080 wsgi
```

A Flask server will start at http://localhost:8080.

- To host this API on cloud instance, follow this step by step procedure: https://pyliaorachel.github.io/blog/tech/system/2017/07/07/flask-app-with-gunicorn-on-nginx-server-upon-aws-ec2-linux.html