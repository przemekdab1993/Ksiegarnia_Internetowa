from flask import Flask, render_template, request, session, json, jsonify
from datetime import datetime
from connectDB import DBco
from random import randint
import time

app = Flask(__name__)

app.secret_key = 'fUrE43v9'

def saveLog(req : 'flask_request', res : str, date : 'datetime') -> None:
	""" Zapisanie logowania do pliku log """
	with open('log/save.log', 'a') as log:
		print(req, res, date, file = log, sep = " || ")
	
def check_status(func):
	""" SPRAWDZANIE CZY JESTEŚ ZALOGOWANY """
	if 'loged_in' in session:
		return func()
	else:
		return render_template('login.html', the_title='Login', the_log='Login')
		
		
@app.route('/')
def hello() -> 'html':
	return "Hello"
	

if __name__ == '__main__':
	app.run(debug = True)
