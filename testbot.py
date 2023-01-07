# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from flask import Flask, request, send_file
import telegram
from credentials import token, domain_name
from tools import booking_links

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
	text = booking_links[link]["text"]
	url = booking_links[link]["url"]
	text_services = text_services + f"{text} <a href='{url}'>{link}</a>\n\n"

directory = "https://visitbudapest.ru/wp-content/uploads/pdf/"

articles = {
	"christmas-markets": "",
}

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

@app.route('/pdf/')
def pdf():
	try:
		return send_file('../webpdf/pdf/1day.pdf')
	except Exception as e:
		return str(e)