# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from flask import Flask, request
import telegram
from auth_data import token
from domain_data import domain_name

app = Flask(__name__)
app.debug = True

TOKEN = token

global bot 
bot = telegram.Bot(token=TOKEN)

URL = domain_name

#WebHook
@app.route('/HOOK', methods=['POST', 'GET']) 
def webhook_handler():
	if request.method == "POST": 
		update = telegram.Update.de_json(request.get_json(force=True), bot)
		try:
			chat_id = update.message.chat.id 
			text = update.message.text
			userid = update.message.from_user.id
			username = update.message.from_user.username
			bot.send_message(chat_id=chat_id, text="hello")
		except Exception as e:
			print(e)
	return 'ok' 

#Set_webhook 
@app.route('/set_webhook', methods=['GET', 'POST']) 
def set_webhook(): 
	s = bot.setWebhook('https://%s:443/HOOK' % URL, certificate=open('/etc/ssl/www/server.crt', 'rb')) 
	if s:
		print(s)
		return "webhook setup ok" 
	else: 
		return "webhook setup failed" 

@app.route("/")
def hello():
	return "Hello"

