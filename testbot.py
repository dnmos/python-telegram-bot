# -*- coding: utf-8 -*-
from flask import Flask, request, send_from_directory
import telegram
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from credentials import token, domain_name
from tools import booking_links
import json

app = Flask(__name__)
app.debug = False

TOKEN = token
URL = domain_name

global bot 
bot = telegram.Bot(TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def Posts_params():
	"""PDF Command send posts PDF list

	Args:
		None
	Returns:
		Posts params json
	"""
	with open('/home/www/webpdf/posts_params.json', 'r') as file:
		result_json = json.load(file)

	return result_json

#WebHook
@app.route('/HOOK', methods=['POST', 'GET']) 
def webhook_handler():
	"""Webhook handler for the telegram bot. If method POST, process Telegram update.

	Args:
		None
	Returns:
		Response text.
	"""
	if request.method == "POST": 
		update = telegram.Update.de_json(request.get_json(force=True), bot)

		dispatcher.process_update(update)

		try:
			text = update.message.text
			chat_id = update.message.chat.id 
			msg_id = update.message.message_id
			userid = update.message.from_user.id
			username = update.message.from_user.username
			userfullname = update.message.from_user.full_name
			posts_params = Posts_params()
			for post in posts_params:
				command = post.replace('-', '_')
				if text == f"/{command}":
					bot.sendDocument(chat_id=chat_id, document=open(f"../webpdf/pdf/{post}.pdf", "rb"))
		except Exception as e:
			print(e)
	return 'ok vbbot' 

@app.route('/set_webhook', methods=['GET', 'POST']) 
def set_webhook(): 
	"""Set webhook for the telegram bot.

	Args:
		None
	Returns:
		Response text.
	"""
	s = bot.setWebhook('https://%s:443/HOOK' % URL, certificate=open('/etc/ssl/www/server.crt', 'rb')) 
	if s:
		print(s)
		return "webhook vbbot setup ok" 
	else: 
		return "webhook vbbot setup failed" 

@app.route('/vb/pdf/<path:name>')
def send_pdf(name):
	"""Send PDF document to the telegram bot.

	Args:
		name: Name of PDF document (document.pdf).
	Returns:
		PDF document.
	"""
	try:
		return send_from_directory('../webpdf/pdf/', name, as_attachment=False)
	except Exception as e:
		return str(e)

def command_handler(command):
	"""Command handler

	Args:
		command: the telegram bot command (/start).
	Returns:
		decorator function with command handler for command
	"""
	def decorator(func):
		handler = CommandHandler(command, func)
		dispatcher.add_handler(handler)
		return func
	return decorator

@command_handler('start')
def start(update=telegram.Update, context=CallbackContext) -> None:
	"""Start Command send start message

	Args:
		update: an incoming Telegram update.
		context: the telegram bot message context.
	Returns:
		None
	"""
	text_start = \
		"Привет! Это бот сайта \nvisitbudapest.ru\n\n"\
		"Бронировать путешествия в Будапеште по лучшим ценам \n/services\n\n"\
		"Скачать статью в PDF \n/pdf"

	context.bot.sendMessage(chat_id=update.message.chat.id, text=text_start)

@command_handler('services')
def services(update=telegram.Update, context=CallbackContext) -> None:
	"""Services Command send message with services list

	Args:
		update: an incoming Telegram update.
		context: the telegram bot message context.
	Returns:
		None
	"""
	text_services = ""
	for link in booking_links:
		service = booking_links[link]["text"]
		url = booking_links[link]["url"]
		text_services += f"{service} <a href='{url}'>{link}</a>\n\n"

	context.bot.sendMessage(chat_id=update.message.chat.id, parse_mode="HTML", text=text_services, disable_web_page_preview=True)

@command_handler('pdf')
def pdf(update=telegram.Update, context=CallbackContext) -> None:
	"""PDF Command send posts PDF list

	Args:
		update: an incoming Telegram update.
		context: the telegram bot message context.
	Returns:
		None
	"""
	posts_params = Posts_params()
	text_posts = "Выберите статью из списка ниже:\n\n"
	for post in posts_params:
		title = posts_params[post]['title']
		command = post.replace('-', '_')
		text_posts = text_posts + title + '\n' + f' /{command}\n\n' 

	context.bot.sendMessage(chat_id=update.message.chat.id, parse_mode="HTML", text=text_posts, disable_web_page_preview=True)