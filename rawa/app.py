from flask import Flask, render_template
from os import environ

from rawa.models import db

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


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
