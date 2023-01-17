# python-telegram-bot

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Initial server setup](#initial-server-setup)
* [Domain name configure](#domain-name-configure)
* [Install nginx](#install-nginx)
* [Python components, virtualenv, gunicorn and flask](#python-components-virtualenv-gunicorn-and-flask)
* [Relative links](#relative-links)

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
	
## Initial server setup
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

## Domain name configure

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
(env) $ nano ~/bot/wsgi.py
```

~/myproject/wsgi.py
```
from myproject import app

if __name__ == "__main__":
    app.run()
```

Step 4 — Configuring Gunicorn

```
(env) $ cd ~/bot
(env) $ gunicorn --bind 0.0.0.0:5000 wsgi:app
```

http://yourserverip:5000

```
(env) $ deactivate
```

Create the systemd service unit file.
```
$ sudo nano /etc/systemd/system/testbot.service
```

/etc/systemd/system/testbot.service
```
[Unit]
Description=Gunicorn instance to serve testbot
After=network.target

[Service]
User=www
Group=www-data
WorkingDirectory=/home/www/bot
Environment="PATH=/home/www/bot/env/bin"
ExecStart=/home/www/bot/env/bin/gunicorn --workers 3 --bind unix:testbot.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

With that, your systemd service file is complete. Save and close it now.

You can now start the Gunicorn service that you created and enable it so that it starts at boot:
```
$ sudo systemctl start testbot
$ sudo systemctl enable testbot
```
Let’s check the status:
```
$ sudo systemctl status testbot
```

Step 5 — Configuring Nginx to Proxy Requests

```
$ sudo nano /etc/nginx/sites-available/testbot
```

/etc/nginx/sites-available/testbot
```
server {
    listen 443 default ssl;
    server_name your_domen your_ip;
    keepalive_timeout 60;
    ssl_certificate /etc/ssl/www/server.crt;
    ssl_certificate_key  /etc/ssl/www/server.key;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers  "HIGH:!RC4:!aNULL:!MD5:!kEDH";
    add_header Strict-Transport-Security 'max-age=604800';
    access_log /var/log/nginx_access.log;
    error_log /var/log/ngingx_error.log;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/www/bot/testbot.sock;
    }
}

server {
    listen 80;

    server_name your_domen your_ip;

    return 302 https://$server_name$request_uri;
}
```

```
$ sudo ln -s /etc/nginx/sites-available/testbot /etc/nginx/sites-enabled
$ sudo nginx -t
$ sudo systemctl restart nginx
```

http://your_domain

If you encounter any errors, trying checking the following:
```
$ sudo less /var/log/nginx/error.log: checks the Nginx error logs.
$ sudo less /var/log/nginx/access.log: checks the Nginx access logs.
$ sudo journalctl -u nginx: checks the Nginx process logs.
$ sudo journalctl -u myproject: checks your Flask app’s Gunicorn logs.
```

Step 6 — Create a Self-Signed SSL Certificate for Nginx in Ubuntu 22.04

```
$ cd /etc/ssl/
$ sudo mkdir www
$ cd www
$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/www/server.key -out /etc/ssl/www/server.crt
```
Fill out the prompts appropriately. The most important line is the one that requests the Common Name (e.g. server FQDN or YOUR name). You need to enter the domain name associated with your server or, more likely, your server’s public IP address.

The entirety of the prompts will look like the following:
```
Output
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:New York
Locality Name (eg, city) []:New York City
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Bouncy Castles, Inc.
Organizational Unit Name (eg, section) []:Ministry of Water Slides
Common Name (e.g. server FQDN or YOUR name) []:server_IP_address
Email Address []:admin@your_domain.com
```

Now, open the configuration file
```
$ sudo nano /etc/nginx/sites-available/testbot
```

```
$ sudo nginx -t
$ sudo service nginx restart
```

```
$ cd ~/bot
$ . ./env/bin/activate
$ sudo pip install python-telegram-bot
```

Launch bot and go to https://yourip/set_webhook.

Restart bot:
```
$ sudo service testbot restart 
```

## Relative links

* https://docs.python-telegram-bot.org/en/v13.15/telegram.ext.html# 
* https://github.com/python-telegram-bot/v13.x-wiki/wiki/Webhooks
* https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04
* https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-22-04#step-2-%E2%80%93-configuring-nginx-to-use-ssl
* http://abdulmadzhidov.ru/blog/Telegram-bot-in-30-min/

