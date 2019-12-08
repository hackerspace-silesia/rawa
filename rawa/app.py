from os import environ

from flask import Flask, render_template, request, session

from rawa.commands.exceptions import CommandError
from rawa.models import db
from rawa.commands.user import find_user, register, login as command_login
from rawa.commands.token import use_token as command_use_token
from rawa.commands.token import find_token, generate_qr_code

DATABASE_URI = environ.get('DATABASE_URI', 'sqlite:///test.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login/')
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = command_login(email, password)
        if user is None:
            return render_template('login.html', failed=True)
        else:
            session['user_id'] = user.id
            return render_template('dashboard.html')


@app.route('/register/')
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            register(email, password)
        except CommandError as exp:
            return render_template('register.html', errs=exp.args[0])
        else:
            return render_template('register_done.html')


@app.route('/use/<token_value:str>')
def use_token(token_value):
    user = find_user(user_id=session['user_id'])
    if not user:
        return '', 401

    try:
        used_token = command_use_token(user, token_value)
    except CommandError as exp:
        return render_template(
            'use_token_error.html',
            errs=exp.args[0],
        )
    else:
        return render_template('use_token_success.html', used_token=used_token)


@app.route('/token/<token_id:int>')
def show_token(token_id):
    token = find_token()
    if not token:
        return '', 404
    code = generate_qr_code(token, prefix='http://')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
