from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import re
app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app,'snippets')
app.secret_key = "13k3dfgdfg78987"



#methods in global scope for modularity to add new features later
def get_user(email):
    user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
    query_data = { 'email': email }
    user = mysql.query_db(user_query, query_data)
    return user




@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/main', methods=['GET', 'POST'])
def wall():
    if request.method == 'GET':

        #get current user dictionary
        current_user = get_user(session['email'])

        #get basic scrubbed info of user
        name = current_user[0]['first_name']
        return render_template('main.html', current_name = name)






@app.route('/create_user', methods=['POST'])
def create():
    print "hit"
    print request.form

#validation for exist done in view with HTML
    first_name = request.form['first_name']
    last_name = request.form['last_name']

#email exist / type validation done in view
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['password_confirm']

#rest of validations
    if len(first_name) <= 2:
        flash("Your name should be greater than 2 characters")
        return redirect('/')
    elif len(last_name) <= 2:
        flash("Your last name should be greater than 2 characters")
        return redirect('/')
    elif len(password) <= 8:
        flash("Your password should be more than 8 characters")
        return redirect('/')
    elif password != confirm:
        flash("Your password and confirmations doesnt match")
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(password)
        insert_query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at) VALUES (:first_name, :last_name, :email, :pw_hash, NOW())"
        query_data = { 'first_name': first_name, 'last_name' : last_name, 'email': email,'pw_hash': pw_hash }
        mysql.query_db(insert_query, query_data)

    #get/set session for user before success page
        user = get_user(email)
        session['id'] = user[0]['id']
        session['name'] = user[0]['first_name']
        session['email'] = user[0]['email']

        return redirect('/main')

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user(email)

        if len(user) != 0 and bcrypt.check_password_hash(user[0]['pw_hash'], password):
            session['id'] = user[0]['id']
            session['name'] = user[0]['first_name']
            session['email'] = user[0]['email']
            return redirect('/main')

        else:
            flash("Please try again")
            return redirect('/login')

    elif request.method == 'GET':
        return render_template('login.html')

#logout user and clear session
@app.route('/logout', methods=['GET'])
def logout():

    if  'id' in session:
        session.pop('id')
        session.pop('name')
        session.pop('email')
        print session
        return redirect('/')

    else:
        flash("Already logged out")
        return redirect('/')

app.run(debug=True)
