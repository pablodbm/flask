from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bs4 import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
import math


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'GNTGT35T1G65TJGYUTUIG3GHWDP'

class NameForm(FlaskForm):
    userName = StringField('Podaj swoje imię: ', validators=[DataRequired()])
    submit = SubmitField('Wyslij')

class Kwadratowa(FlaskForm):
    a = IntegerField("Podaj a", validators=[DataRequired()])
    b = IntegerField("Podaj b", validators=[DataRequired()])
    c = IntegerField("Podaj c", validators=[DataRequired()])
    submit = SubmitField("Oblicz")

@app.route('/')
def index():
    userForm = NameForm()
    return render_template('index.html', title="Strona głowna", currentTime=datetime.utcnow(), userForm=userForm)

@app.route('/user', methods=['POST'])
def userName():
    userName = request.form['userName']
    return render_template('user.html', title="Użytkownik", userName=userName)
@app.route('/user/<name>')
def user(name):
    return render_template('index.html', title="Uzytkownik", name=name)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404
@app.errorhandler(500)
def internal(error):
    return render_template('500.html', title='500'), 500

@app.route("/setSession", methods=['POST','GET'])
def setSession():
    userForm = NameForm()
    if userForm.validate_on_submit():
        oldName = session.get('userName')
        if oldName is not None and userName != userForm.userName.data:
            flash("Zmieniłeś swoje imie")
        session['userName'] = userForm.userName.data
        return redirect(url_for('setSession'))
    return render_template('session.html', title='Zastosowanie sesji', userForm= userForm, userName=session.get('userName'))

@app.route('/function', methods=['POST','GET'])
def function():
    userForm = Kwadratowa()
    message = ""
    if userForm.validate_on_submit():
        a = userForm.a.data
        if a == 0:
            message = "Funkcja liniowa"
        else:
            b = userForm.b.data
            c = userForm.c.data
            delta = math.pow(b, 2) - 4*a*c
            if delta > 0:
                x1 = (-b + math.sqrt(delta)) / 2*a
                x2 = (-b - math.sqrt(delta)) / 2*a
                message = "Miejsca zerowe funkcji x1 = " + str(round(x1, 2)) + " i x2 = " + str(round(x2, 2))
            elif delta == 0:
                x1 = -b/2*a
                message = "Jedno miejsce zerowe x1 = " + str(round(x1, 2))
            else:
                message = "Brak miejsc zerowych"

    return render_template('function.html', title='Miejsca zerowe', userForm=userForm, message=message)

if __name__ == '__main__':
    app.run(debug=True)