from flask import Flask, escape, request, render_template

app = Flask(__name__)


@app.route('/')
def home(name=None):
    return render_template('home.html', name=name)


@app.route('/login/')
def login(name=None):
    return render_template('login.html', name=name)


@app.route('/register/')
def register(name=None):
    return render_template('register.html', name=name)






