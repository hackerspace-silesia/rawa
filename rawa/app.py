from flask import Flask, escape, request
from os import environ

from rawa.models import db

DATABASE_URI = environ.get('DATABASE_URI', 'sqlite:///test.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI


@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    return f'Hello, {escape(name)}!'


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
