from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key='seocho30#'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'kaist30#'
app.config['MYSQL_DB'] = 'pythonlogin'

mysql = MySQL(app)

@app.route('/pythonlogin', methods=['GET','POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			return '성공적으로 로그인 되셨습니다'
		else:
			msg = 'Incorrect username/password!'
	
	return render_template('index.html', msg=msg)

if __name__ == '__main__':
	app.run(debug=True)

