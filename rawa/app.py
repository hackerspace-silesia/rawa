from flask import Flask, render_template, request, session
from os import environ
from rawa.commands.exceptions import CommandError
from rawa.models import db
from rawa.commands.user import register, login as command_login

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


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
