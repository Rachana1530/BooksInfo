
from flask import Flask, render_template, request, redirect ,session
import mysql.connector
import os
app = Flask(__name__)
app.secret_key=os.urandom(24)
conn = mysql.connector.connect(host="localhost", user="root", password="",database="bookstore1")
cursor=conn.cursor()

@app.route('/')
def login():

    return render_template('login.html')

@app.route('/register')
def about():
     return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:

        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    Email=request.form.get('email')
    Password=request.form.get('password')
    cursor.execute("""SELECT * FROM users WHERE Cemail LIKE '{}' AND Cpassword LIKE '{}'"""
               .format(Email, Password))

    users=cursor.fetchall()
    if len(users)>0:
        session['user_id'] = users[0][1]
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/categories')
def categories():
       return render_template('/categories.html')

@app.route('/bookstore')
def bookstore():
    return render_template('/bookstore.html')


@app.route('/add_user',methods=['POST'])
def add_user():
    name = request.form.get('cname')
    email = request.form.get('cemail')
    password = request.form.get('cpassword')
    contact = request.form.get('cphone')
    cursor.execute("""INSERT INTO users (Cname,Cemail,Cpassword,Ccontact) VALUES 
    ('{}','{}','{}','{}')""".format(name, email, password, contact))
    conn.commit()
    cursor.execute("""SELECT * FROM users WHERE Cemail LIKE '{}'""".format(email))
    mycur=cursor.fetchall()
    session['user_id']=mycur[0][1]
    return redirect('/home')


@app.route('/create')
def create():
    return redirect("Added new book in store")

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)


