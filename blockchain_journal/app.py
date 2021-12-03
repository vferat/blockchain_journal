from functools import wraps
from flask import Flask, render_template, redirect, url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from models import UserModel, db, login

from populate_db import populate_database


app = Flask(__name__)
app.secret_key = '123'

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()
    populate_database(db)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return UserModel.query.filter_by(id=id).first()


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template('test.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')   

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('test'))
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        print(UserModel.query.filter_by(email=email).first())
        if UserModel.query.filter_by(email=email).first() is not None:
            return ('Email already Present')
             
        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/author/<username>', methods=['GET'])
def author(username):
    print('request')
    if request.method == 'GET':
        user = UserModel.query.filter_by(username=username).first()
        if user is not None:
            papers = user.papers
            dois = [paper.doi for paper in papers]
            return render_template('paper.html', dois=dois)
        else:
            return redirect(url_for('index'))

app.run(port=8080, debug=True, ssl_context='adhoc')