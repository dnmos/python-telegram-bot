# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from flask import Flask, request, send_from_directory
import telegram
from credentials import token, domain_name
from tools import booking_links
import json

app = Flask(__name__)
app.debug = True

TOKEN = token
URL = domain_name

global bot 
bot = telegram.Bot(token=TOKEN)

text_start = \
	"Привет! Это бот сайта \nvisitbudapest.ru\n\n"\
	"Бронировать путешествия в Будапеште по лучшим ценам \n/services\n\n"\
	"Скачать статью в PDF \n/pdf"

text_services = ""
for link in booking_links:
	service = booking_links[link]["text"]
	url = booking_links[link]["url"]
	text_services += f"{service} <a href='{url}'>{link}</a>\n\n"

with open('/home/www/webpdf/posts_params.json', 'r') as file:
	posts_params = json.load(file)
text_posts = "Выберите статью из списка ниже:\n\n"
for post in posts_params:
	title = posts_params[post]['title']
	command = post.replace('-', '_')
	text_posts = text_posts + title + '\n' + f' /{command}\n\n' 

#WebHook
@app.route('/HOOK', methods=['POST', 'GET']) 
def webhook_handler():
	if request.method == "POST": 
		update = telegram.Update.de_json(request.get_json(force=True), bot)
		try:
			chat_id = update.message.chat.id 
			msg_id = update.message.message_id
			text = update.message.text
			userid = update.message.from_user.id
			username = update.message.from_user.username
			userfullname = update.message.from_user.full_name
			if text == "/start":
				bot.sendMessage(chat_id=chat_id, text=text_start)
			elif text == "/services":
				bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text_services, disable_web_page_preview=True)
			elif text == "/pdf":
				bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text_posts, disable_web_page_preview=True)
			else:
				for post in posts_params:
					command = post.replace('-', '_')
					if text == f"/{command}":
						bot.sendDocument(chat_id=chat_id, document=open(f"../webpdf/pdf/{post}.pdf", "rb"))
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

@app.route('/pdf/<path:name>')
def send_pdf(name):
	try:
		return send_from_directory('../webpdf/pdf/', name, as_attachment=False)
	except Exception as e:
		return str(e)

