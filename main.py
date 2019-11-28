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

@app.route('/pythonlogin/home')
def home():
	if 'loggedin' in session:
		return render_template('home.html', username=session['username'])
	return redirect(url_for('login'))

@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))



@app.route('/pythonlogin', methods=['GET','POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', [username, password])
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			return redirect(url_for('home')) 
		else:
			msg = '비밀번호가 다릅니다. 다시 확인해 주세요.'
	
	return render_template('index.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/pythonlogin/register', methods=['GET','POST'])
def register():
	msg=''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = %s', [username])
		account = cursor.fetchone()
		if account:
			msg = '아이디가 중복이 됩니다. 다시 입력해 주세요.'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = '유효하지 않는 이메일 주소입니다.'
		#elif not re.match(r'[A-Za-z0-9]+', username):
			#msg = '한글이나 특수문자는 입력가능 합니다.영문과 숫자만 가능합니다.'
		elif not username or not password or not email:
			msg = '회원가입란에 작성을 해주세요'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', [username, password, email])
			mysql.connection.commit()
			msg = '성공적으로 가입이 완료되었습니다.'
	elif request.method == 'POST':
		msg = '회원가입란에 작성을 해주세요'
	return render_template('register.html', msg=msg)

if __name__ == '__main__':
	app.run(debug=True)

