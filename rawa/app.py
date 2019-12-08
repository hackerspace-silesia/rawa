from os import environ
from io import BytesIO

from flask import Flask, render_template, request, session, send_file, redirect

from rawa.commands.exceptions import CommandError
from rawa.commands.prize import get_all_prizes, get_bought_prizes, \
    find_prize
from rawa.commands.prize import buy_prize as command_buy_prize
from rawa.models import db
from rawa.commands.user import find_user, compute_stats
from rawa.commands.user import register as command_register
from rawa.commands.user import login as command_login
from rawa.commands.token import use_token as command_use_token
from rawa.commands.token import find_token, generate_qr_code

DATABASE_URI = environ.get('DATABASE_URI', 'sqlite:///test.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.secret_key = 'karolina'
db.init_app(app)


@app.route('/')
def home():
    user = find_user(session.get('user_id'))
    if user is not None:
        return dashboard(user)
    return render_template('home.html')


def dashboard(user):
    score, used_tokens_count = compute_stats(user)
    return render_template(
        'dashboard.html',
        score=score,
        used_tokens_count=used_tokens_count,
        user=user,
    )


@app.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = command_login(email, password)
    if user is None:
        return render_template('login.html', failed=True)
    else:
        session['user_id'] = user.id
        return redirect('/')


@app.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/logout', methods=['GET'])
def logout():
    del session['user_id']
    return redirect('/')


@app.route('/register/', methods=['POST'])
def register_post():
    email = request.form['email']
    password = request.form['password']
    try:
        command_register(email, password)
    except CommandError as exp:
        return render_template('register.html', errs=exp.args[0])
    else:
        return render_template('register_done.html')


@app.route('/unathorized/', methods=['GET'])
def unauthorize():
    return render_template('unauthorized.html')


@app.route('/use/<token_value>')
def use_token(token_value):
    user = find_user(user_id=session.get('user_id'))
    if not user:
        return redirect('/unathorized')
    try:
        used_token = command_use_token(user, token_value)
    except CommandError as exp:
        return render_template(
            'use_token/error.html',
            errs=exp.args[0],
        )
    else:
        return render_template('use_token/success.html', used_token=used_token)


@app.route('/token/<token_id>')
def show_token(token_id):
    token = find_token(int(token_id))
    if not token:
        return '', 404
    img_io = BytesIO()
    img = generate_qr_code(token, prefix='http://172.50.2.67:5000/use/')
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


def _show_prizes(user, message=None):
    score, _ = compute_stats(user)
    all_prizes = get_all_prizes()
    bought_prizes = get_bought_prizes(user)
    return render_template(
        'prize.html',
        user=user,
        message=message,
        available_prizes=all_prizes,
        bought_prizes=bought_prizes,
    )

@app.route('/prizes')
def show_prizes():
    user = find_user(user_id=session.get('user_id'))
    if not user:
        return redirect('/unathorized')
    return _show_prizes(user)


@app.route('/prize/<prize_id>')
def buy_prize(prize_id):
    user = find_user(user_id=session.get('user_id'))
    if not user:
        return redirect('/unathorized')
    prize = find_prize(int(prize_id))
    if not prize:
        return '', 404

    command_buy_prize(user, prize)
    return _show_prizes(user, message=f'Kupiłeś "{prize.name}"!')

if __name__ == '__main__':
    app.run(debug=True)
