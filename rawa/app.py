from flask import Flask, render_template, session
from os import environ

from rawa.commands.exceptions import CommandError
from rawa.models import db
from rawa.commands.user import find_user
from rawa.commands.token import use_token as command_use_token
from rawa.commands.token import find_token, generate_qr_code

DATABASE_URI = environ.get('DATABASE_URI', 'sqlite:///test.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI


@app.route('/')
def home(name=None):
    return render_template('home.html', name=name)


@app.route('/login/')
def login(name=None):
    return render_template('login.html', name=name)


@app.route('/register/')
def register(name=None):
    return render_template('register.html', name=name)


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
