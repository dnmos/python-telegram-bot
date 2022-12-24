# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
from flask import Flask, request
import telegram
from credentials import token, domain_name

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

booking_links = {
	"aviasales"       : "https://aviasales.tp.st/UjGdnswh",
	"ostrovok"        : "https://ostrovok.tp.st/AAuVl11s",
	"budapest-card"   : "https://getyourguide.tp.st/lb1gHBuo",
	"music"           : "https://getyourguide.tp.st/FPLOTyuR",
	"hop-on-hop-off"  : "https://getyourguide.tp.st/9XbNgvn4",
	"szechenyi" : "https://getyourguide.tp.st/8BJxp83p",
	"cruises"         : "https://getyourguide.tp.st/yl94pXIX",
	"szentendre"      : "https://tripster.tp.st/FWI4AlO4",
	"cherehapa"       : "https://cherehapa.tp.st/sBWDO7e5",
	"auto"            : "https://economybookings.tp.st/3gksCIJ2",
	"kiwitaxi"        : "https://kiwitaxi.tp.st/mucJFLwZ",
	"tripster"        : "https://tripster.tp.st/mojAh9jY",
	"level"           : "https://level.tp.st/1kTUYtSy",
	"sanatoriums"     : "https://sanatoriums.tp.st/OASrIX6y",
	"getyourguide"    : "https://getyourguide.tp.st/eGqlK7Rp",
	"drimsim"         : "https://drimsim.tp.st/XsVNrhNk",
}

text_services = \
	f"Авиабилеты <a href='{booking_links['aviasales']}'>aviasales</a>\n\n"\
	f"Отели <a href='{booking_links['ostrovok']}'>ostrovok</a>\n\n"\
	f"BudapestCard <a href='{booking_links['budapest-card']}'>budapest-card</a>\n\n"\
	f"Мюзиклы и шоу <a href='{booking_links['music']}'>music</a>\n\n"\
	f"Hop On Hop Off <a href='{booking_links['hop-on-hop-off']}'>hop-on-hop-off</a>\n\n"\
	f"Купальня Сечени <a href='{booking_links['szechenyi']}'>szechenyi</a>\n\n"\
	f"Круизы по Дунаю <a href='{booking_links['cruises']}'>cruises</a>\n\n"\
	f"Сентендре <a href='{booking_links['szentendre']}'>szentendre</a>\n\n"\
	f"Страховка <a href='{booking_links['cherehapa']}'>cherehapa</a>\n\n"\
	f"Аренда авто <a href='{booking_links['auto']}'>auto</a>\n\n"\
	f"Трансферы <a href='{booking_links['kiwitaxi']}'>kiwitaxi</a>\n\n"\
	f"Экскурсии <a href='{booking_links['tripster']}'>tripster</a>\n\n"\
	f"Туры <a href='{booking_links['level']}'>level</a>\n\n"\
	f"Санатории <a href='{booking_links['sanatoriums']}'>sanatoriums</a>\n\n"\
	f"Входные билеты <a href='{booking_links['getyourguide']}'>getyourguide</a>\n\n"\
	f"Сим-карта <a href='{booking_links['drimsim']}'>drimsim</a>\n\n"

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