from flask import Flask, render_template, session, redirect
from flask_bs4 import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired
import math


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'GNTGT35T1G65TJGYUTUIG3GHWDP'

class LoginForm(FlaskForm):
    userLogin = StringField("Nazwa użytkownika:", validators=[DataRequired()])
    userPassword = PasswordField("Hasło:", validators=[DataRequired()])
    submit = SubmitField("Zaloguj")

users = {
    1:{
        'userLogin':'kacper',
        'userPass':'123qweasd',
        'firstName':'Kacper',
        'lastName':'Nowak'
    },
}

@app.route('/')
def index():
    return render_template('index.html', title="Strona głown")

@app.route('/login', method=["POST","GET"])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        userLogin = loginForm.userLogin.data
        userPassword = loginForm.userPassword.data
        if(userLogin == users[1]['userLogin'] and userPassword == users[1]['userPass']):
            session['userLogin'] = userLogin
            return redirect('dashboard')
    return render_template("login.html", title="Logowanie", form=loginForm, userLogin=session.get('userLogin'))

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard", title="Dashboard", userLogin=session.get("userLogin"))


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404
@app.errorhandler(500)
def internal(error):
    return render_template('500.html', title='500'), 500


if __name__ == '__main__':
    app.run(debug=True)