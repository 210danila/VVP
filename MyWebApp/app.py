import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="1234",
                        host="localhost",
                        port="5432")

cursor = conn.cursor() 


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')   
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            print(records)

            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/', methods=['GET'])
def main():
    return redirect('/login/')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    is_reg = 'Create your account :'
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        print(name, login, password)
        cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(login), str(password)))
        records1 = list(cursor.fetchall())

        if request.form.get('name') == '' or request.form.get('login') == '' or request.form.get('password') == '':
            is_reg = 'type your name, login and password'
        elif  records1 != []:
            is_reg = 'This login is already in use'

        else:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
            conn.commit()

            return redirect('/login/')


    return render_template('registration.html', is_reg=is_reg)