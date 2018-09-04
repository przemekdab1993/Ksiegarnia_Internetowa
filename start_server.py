from flask import Flask, render_template, request, session
from datetime import datetime
from connectDB import DBco
from random import randint
from decimal import Decimal
import time


app = Flask(__name__)

app.secret_key = 'fUrE43v9'
dbconfig = { 'host': '127.0.0.1',
			'user': 'root',
			'password': 'root',
			'database': 'ksiegarnia_internetowa', }



def saveLog(req : 'flask_request', res : str, date : 'datetime') -> None:
	''' Zapisanie logowania do pliku log '''
	with open('log/save.log', 'a') as log:
		print(req, res, date, file = log, sep = " || ")
	
def check_status(func):
	''' SPRAWDZANIE CZY JESTEŚ ZALOGOWANY '''
	if 'loged_in' in session:
		return func()
	return render_template('login.html', the_title= 'Login')
		
		
''' ----------------------------- '''
''' STRONA GŁÓWNA I JEJ PODSTRONY '''	
''' ----------------------------- '''		
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
			
	return render_template('book_info.html', the_info = res, the_title = res[0][1])

	
''' ----------------------------------- '''
''' LOGOWANIE I REJESTRACJA UŻYTKOWNIKA '''	
''' ----------------------------------- '''	
@app.route('/login')
def login() -> 'html':
	if 'loged_in' in session:
		with DBco(dbconfig) as cursor:
			_SQL = """ SELECT id_user, email FROM user WHERE id_user = (%s) """
			cursor.execute(_SQL, (session['id_user'],))
			res = cursor.fetchone()
		temp_res = {'user_name': session['user_name'], 'id_user': res[0], 'email': res[1]}
		return render_template('settings.html', the_res = temp_res , the_title = 'Dane użytkownika')
	else:
		return render_template('login.html', the_title = 'Logowanie')
		
@app.route('/login_up', methods=['POST'])
def login_up() -> 'html':
	user_name = request.form['user_name']
	password = request.form['password']
	with DBco(dbconfig) as cursor:
		_SQL = """SELECT id_user FROM user WHERE user_name = (%s) AND password = (%s) """
		cursor.execute(_SQL, (user_name, password, ))
		res = cursor.fetchone()	
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
			_SQL = """ INSERT INTO user (user_name, password, email, cash) VALUES (%s, %s, %s, %s) """
			cursor.execute(_SQL, (user_name, password_1, email, '0'))
		return render_template('login.html', the_script = 'sucess_regist.js', the_title = "Tak")
	else:
		return render_template('registration.html', the_title = "Nie")

		
''' ----------------------- '''
''' ------- PORTFEL ------- '''	
''' ----------------------- '''		
def show_cash() -> str:
	with DBco(dbconfig) as cursor:
		_SQL = """ SELECT cash FROM user WHERE id_user = (%s) """
		cursor.execute(_SQL, (session['id_user'],))
		res = cursor.fetchall()
		for i in res:
			for j in i:
				res = j
	return res

@app.route('/my_wallet')
def my_wallet() -> 'html':
	def wallet() -> 'html':
		with DBco(dbconfig) as cursor:
			_SQL = """ SELECT * FROM transactions WHERE id_user = (%s) ORDER BY data_order DESC"""
			cursor.execute(_SQL, (session['id_user'],))
			res = cursor.fetchall()
		return render_template('wallet.html', the_res = res, the_cash = show_cash(), the_title = "Portfel")
	return check_status(wallet)

	return False
	
def select_data_book(id_book) -> tuple:
	with DBco(dbconfig) as cursor:
		_SQL = """ SELECT tytul, cena FROM ksiazki WHERE id_ksiazki = (%s) """
		cursor.execute(_SQL, (id_book,))
		rex = cursor.fetchone()
	return rex
	
@app.route('/buy_new-action=<id_book>')
def buy_new(id_book : str) -> 'html':
	''' STRONA Kupowanie nowej ksiazki '''
	def buy() -> 'html':
		if (check_book_list(id_book)) == True:
			return render_template('alert.html', the_res = "Posiadasz już tą książke w swojej kolekcji.", the_title = "Błąd")
		res = select_data_book(id_book)
		data_buy = {'id_book' : id_book, 'title' : res[0], 'cash' : show_cash(), 'price' : res[1], 'result' : (show_cash() - res[1])}
		
		return render_template('new_transaction.html', the_res_buy = data_buy, the_cash = data_buy['cash'], the_title = "Kupuj")
	
	return check_status(buy)

@app.route('/book-buy_new-<id_book>')
def book_buy_add(id_book : str) -> 'html':
	def add_book() -> 'html':
		res = select_data_book(id_book)
		for r in res:
			book_title = res[0]
			book_price = res[1]
			
		user_cash = show_cash()
		
		if user_cash >= book_price:
			new_user_cash = user_cash - book_price
			with DBco(dbconfig) as cursor:
				_SQL1 = """ UPDATE user SET cash = %s WHERE id_user = %s """ 
				cursor.execute(_SQL1, (new_user_cash, session['id_user']))
	
				_SQL2 = """ INSERT INTO transactions (id_ksiazki, id_user, name, cost) VALUES (%s, %s, %s, %s) """
				cursor.execute(_SQL2, (id_book, session['id_user'], book_title, book_price))
				
			return render_template('alert.html',the_res = "Gratujacje pomyślnego dokonania zakupu. Możesz teraz z niego korzystać.", the_title = "Potwierdzenie")
		else:
			return render_template('alert.html',the_res = "Niestety nie posiadasz wystarczającej illości środków w swoim portfelu. Doładuj konto.", the_title = "Niepowodzenie")
	return check_status(add_book)
	
if __name__ == '__main__':
	app.run(debug = True)
	