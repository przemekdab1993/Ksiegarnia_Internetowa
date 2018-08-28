from flask import Flask, render_template, request, session
from datetime import datetime
from connectDB import DBco
from random import randint
import time

app = Flask(__name__)

dbconfig = { 'host': '127.0.0.1',
			'user': 'root',
			'password': 'root',
			'database': 'ksiegarnia_internetowa', }

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
		return render_template('login.html', the_title= 'Login')
		
		
@app.route('/')
def hello() -> 'html':
	with DBco(dbconfig) as cursor:
			_SQL = """SELECT id_ksiazki, tytul, gatunek, ocena FROM ksiazki """
			cursor.execute(_SQL)
			res = cursor.fetchall()
	return render_template('home.html', the_books = res, the_title = "Książki")
	
@app.route('/book_info<id_book>')
def info(id_book : str) -> 'html':
	with DBco(dbconfig) as cursor:
			_SQL = """SELECT * FROM ksiazki AS k, ksiazki_information AS i WHERE k.id_ksiazki = i.id_ksiazki AND k.id_ksiazki = (%s) """
			cursor.execute(_SQL, (id_book,))
			res = cursor.fetchall()
			
	return render_template('book_info.html', the_info = res, the_title = res)
	
@app.route('/login')
def login() -> 'html':
	if 'loged_in' in session:
		return ("Jesteś już zalogowany jako " + session['user_name'])
	else:
		return render_template('login.html', the_title = 'Logowanie')
		
@app.route('/login_up', methods=['POST'])
def login_up() -> 'html':
	user_name = request.form['user_name']
	password = request.form['password']
	session['loged_in'] = True
	session['user_name'] = user_name
	return ('Jesteś teraz zalogowany jako ' + user_name + password)
	
@app.route('/login_down')
def login_down() -> 'html':
	session.clear()
	return "wylogowany"
	
@app.route('/my_wallet')
def my_wallet() -> 'html':
	def wallet() -> str:
		return "portfel a w portfelu 0"
	return check_status(wallet)
		
if __name__ == '__main__':
	app.run(debug = True)