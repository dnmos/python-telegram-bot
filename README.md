# python-telegram-bot

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
Python telegram bot (Web hook)
	
## Technologies
Project is created with:
* Ubuntu 22.04
* Python3.10
* nginx/1.18.0
* gunicorn-20.1.0
* Flask-2.2.2
* python-telegram-bot-13.15
	
## Initial Server Setup with Ubuntu 22.04
Ubuntu 22.04 VPS https://beget.com/ru/cloud/marketplace/ubuntu-22-04

```
$ ssh root@0.0.0.0
$ adduser www
$ adduser www sudo
$ exit
$ ssh-copy-id www@0.0.0.0
$ ssh www@0.0.0.0
$ sudo nano /etc/ssh/sshd_config
AllowUsers www
PermitRootLogin no
PasswordAuthentication no
$ sudo service ssh restart 
```

## A domain name configure to point to your server

Purchase domains. Be sure to create the following DNS records:

* An A record with your_domain pointing to your server’s public IP address.
* An A record with www.your_domain pointing to your server’s public IP address.


## Install nginx

```
$ apt update 
$ sudo apt install nginx
```

## Python components, virtualenv, gunicorn and flask

Step 1 — Installing the Components from the Ubuntu Repositories
```
$ sudo apt update
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```

Step 2 — Creating a Python Virtual Environment
```
$ sudo apt install python3-venv
$ mkdir ~/bot
$ cd ~/bot
$ python3 -m venv env
$ . ./env/bin/activate
```

Step 3 — Setting Up a Flask Application
```
$ pip install wheel
(env) $ pip install gunicorn flask
(env) $ nano ~/bot/testbot.py
```

~/bot/testbot.py
```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello"
```

Test Flask app
```
$ python testbot.py
```

http://yourserverip:5000

Creating the WSGI Entry Point
```
(env) $ nano ~/myproject/wsgi.py
```

~/myproject/wsgi.py
```
from myproject import app

if __name__ == "__main__":
    app.run()
```

Step 4 — Configuring Gunicorn

```
(env) $ cd ~/myproject
(env) $ gunicorn --bind 0.0.0.0:5000 wsgi:app
```

http://yourserverip:5000

```
(env) $ deactivate
```


