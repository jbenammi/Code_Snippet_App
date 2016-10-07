from flask import Flask, request, redirect, render_template, session, flash,jsonify
from mysqlconnection import MySQLConnector
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import re
import jinja2_highlight

class MyFlask(Flask):
    jinja_options = dict(Flask.jinja_options)
    jinja_options.setdefault('extensions',
        []).append('jinja2_highlight.HighlightExtension')

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

def get_snippets(user_id):
    user_query = "SELECT * FROM snippets WHERE user_id = :id"
    query_data = { 'id': user_id }
    user_snippets = mysql.query_db(user_query, query_data)
    return user_snippets



@app.route('/', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/home', methods=['GET'])
def index():
        #get current user dictionary
        current_user = get_user(session['email'])

        #get basic scrubbed info of user
        name = current_user[0]['first_name']

        #get all snippets
        query = "SELECT * FROM snippets WHERE user_id = :id"
        data = {'id' : session['id']}

        snippets = mysql.query_db(query, data)
        return render_template('index.html', current_name = name, all_snippets=snippets)

@app.route('/notes/html', methods=['GET'])
def show_all():
        #get current user dictionary
        current_user = get_user(session['email'])

        #get basic scrubbed info of user
        name = current_user[0]['first_name']

        #get all snippets
        query = "SELECT * FROM snippets WHERE user_id = :id ORDER BY created_at desc"
        data = {'id' : session['id']}

        snippets = mysql.query_db(query, data)
        return render_template('partials/snippets.html', current_name = name, all_snippets=snippets)

@app.route('/notes/form', methods=['GET'])
def show_form():
        return render_template('partials/form.html')

@app.route('/notes/update_form', methods=['GET'])
def update_form():
        return render_template('partials/update_form.html')

@app.route('/create', methods=['POST'])
def create_snippet():

        print request.form

        #get form data
        language = request.form['language']
        code = request.form['code']
        description = request.form['description']


        #query DB
        query = "INSERT INTO snippets(language, code, description, user_id, created_at, updated_at) VALUES(:language, :code, :description, :user_id, NOW(), NOW())"
        query_data = {'language' : language, 'code' : code, 'description' : description, 'user_id' : session['id']}
        mysql.query_db(query, query_data)

        return redirect('/home')

@app.route('/delete', methods=['POST'])
def delete_snippet():
    print request.form

    #get form data
    snippet_id = request.form['snippet-id']

    query = "DELETE FROM snippets WHERE id = :id"
    data = {'id' : snippet_id}
    mysql.query_db(query, data)

    return redirect('/home')


@app.route('/update', methods=['POST'])
def update_snippet():
    print request.form

    #get form data
    snippet_id = request.form['snippet_id']
    code = request.form['code']
    description = request.form['description']
    language = request.form['language']

    #update snippet
    query = "UPDATE snippets SET code = :code, description = :description, language = :language, updated_at = NOW() WHERE id = :id"
    data = {'code' : code, 'description' : description, 'language' : language, 'id' : snippet_id}
    mysql.query_db(query, data)

    return redirect('/home')



@app.route('/get_update', methods=['POST'])
def get_update_snippet():

    #get form data
    snippet_id = request.form['snippet-id']

    #get message from DB
    query = "SELECT * FROM snippets WHERE id = :snippet_id"
    data = {'snippet_id' : snippet_id}

    cur_snippet = mysql.query_db(query, data)

    return jsonify(cur_snippet=cur_snippet[0])

@app.route('/snippets/index_json')
def index_json():
    query = "SELECT * FROM snippets WHERE user_id = :id"
    data = {"id" : session['id']}
    user_snippets = mysql.query_db(query, data)
    return jsonify(all_snippets = user_snippets)

@app.route('/create_user', methods=['POST'])
def create():

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

        return redirect('/home')

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
            return redirect('/home')

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
        return redirect('/home')

app.run(debug=True)
