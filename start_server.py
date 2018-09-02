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
	''' Zapisanie logowania do pliku log '''
	with open('log/save.log', 'a') as log:
		print(req, res, date, file = log, sep = " || ")
	
def check_status(func):
	''' SPRAWDZANIE CZY JESTEŚ ZALOGOWANY '''
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
		return render_template('settings.html', the_user_name = session['user_name'], the_title = 'Dane użytkownika')
	else:
		return render_template('login.html', the_title = 'Logowanie')
		
@app.route('/login_up', methods=['POST'])
def login_up() -> 'html':
	user_name = request.form['user_name']
	password = request.form['password']
	with DBco(dbconfig) as cursor:
		_SQL = """SELECT id_user FROM user WHERE user_name = (%s) AND password = (%s) """
		cursor.execute(_SQL, (user_name, password, ))
		res = cursor.fetchall()	
	if len(res) > 0:
		session['loged_in'] = True
		session['user_name'] = user_name
		session['id_user'] = res[0]
		text = "Jesteś zalogowany jako " + user_name
		return render_template('alert.html', the_res = text, the_title = 'Witam')
	else:
		return render_template('login.html', the_title = 'Logowanie')
	
@app.route('/login_down')
def login_down() -> 'html':
	time.sleep(4)
	session.clear()
	return render_template('alert.html', the_res = "Zostałeś wylogowany", the_title = 'Wylogowanie')
	
@app.route('/registration')
def registration() -> 'html':
	session.clear()
	return render_template('registration.html', the_title = "Rejestracja")

@app.route('/regist_UNX', methods=['POST'])
def reg_UNX() -> 'html':
	user_name = request.form['user_name']
	password_1 = request.form['password_1']
	password_2 = request.form['password_2']
	email = request.form['email']
	flag = True;
	
	''' SPRAWDZANIE POPRAWNOŚCI WPISANYCH DANYCH W FORMULARZU REJESTRACYJNYM '''
	
	''' Sprawdzanie user_name '''
	if (len(user_name) < 4 or len(user_name) > 32):
		flag = False
	with DBco(dbconfig) as cursor:
		_SQL = """SELECT user_name FROM user WHERE user_name = (%s) """
		cursor.execute(_SQL, (user_name, ))
		res = cursor.fetchall()
	lenght_res = len(res)
	if lenght_res != 0:
		flag = False
		
	''' Sprawdzanie password '''
	if password_1 != password_2:
		flag = False
	if (len(password_1)	< 5 or len(password_1) > 16):
		flag = False
		
	''' Sprawdzanie email '''
	buf_x = email.count("@")
	if buf_x != 1:
		flag = False
	else:
		if "." not in email:
			flag = False
		else:
			buf_l = email.index("@")
			after = email[buf_l:]
			if "." not in after:
				flag = False
	with DBco(dbconfig) as cursor:
		_SQL = """ SELECT email FROM user WHERE email = (%s) """
		cursor.execute(_SQL, (email, ))
		res = cursor.fetchall()
	lenght_res = len(res)
	if lenght_res != 0:
		flag = False
		
	''' WYNIK SPRAWDZANIA '''
	'''	Rejestracja nowego urzytkownika lub powrót do formlarza '''
	if flag == True:
		with DBco(dbconfig) as cursor:
			_SQL = """ INSERT INTO user (user_name, password, email, cash) VALUES (%s, %s, %s, %s)"""
			cursor.execute(_SQL, (user_name, password_1, email, '0'))
		return render_template('login.html', the_script = 'sucess_regist.js', the_title = "Tak")
	else:
		return render_template('registration.html', the_title = "Nie")


		
def show_cash() -> str:
	with DBco(dbconfig) as cursor:
		_SQL = """ SELECT cash FROM user WHERE id_user = (%s) """
		cursor.execute(_SQL, (session['id_user']))
		res = cursor.fetchall()
		for i in res:
			for j in i:
				res = j
	return res

@app.route('/my_wallet')
def my_wallet() -> 'html':
	def wallet() -> 'html':
		with DBco(dbconfig) as cursor:
			_SQL = """ SELECT * FROM transactions WHERE id_user = (%s) LIMIT 11 """
			cursor.execute(_SQL, (session['id_user']))
			res = cursor.fetchall()
		return render_template('wallet.html', the_res = res, the_cash = show_cash(), the_title = "Portfel")
	return check_status(wallet)

@app.route('/buy_new')
def buy_new() -> 'html':
	''' STRONA Kupowanie nowej ksiazki '''
	def buy() -> 'html':
		return render_template('new_transaction.html', the_cash = show_cash(), the_title = "Kupuj")
	return check_status(buy)
		
if __name__ == '__main__':
	app.run(debug = True)