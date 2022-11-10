import json
from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_bs4 import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

app: Flask = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
date = datetime.now()
app.config['SECRET_KEY'] = 'klghb6iu#$%&h5uioeqy28689ot46735ehklyg5yu1t'


class Form(FlaskForm):
    city = StringField('Miasto:', validators=[DataRequired()])
    submit = SubmitField('Wyślij')


@app.route('/', methods=['POST', 'GET'])
def index():
    form = Form()
    if form.validate_on_submit():
        city = form.city.data
        print(city)
        with open('data/weather.json', encoding="utf-8") as weatherFiles:
            weatherData = json.load(weatherFiles)
            weatherFiles.close()
        for data in weatherData:
            if data["stacja"] == city:
                return render_template('weather.html', title="Strona głowna", userForm=form,
                                       dataPomiaru=data["data_pomiaru"],
                                       godzinaPomiaru=data["godzina_pomiaru"], temperatura=data["temperatura"],
                                       predkoscWiatru=data["predkosc_wiatru"], kierunekWiatru=data["kierunek_wiatru"],
                                       wilgotnoscWzgledna=data["wilgotnosc_wzgledna"], sumaOpadu=data["suma_opadu"],
                                       cisnienie=data["cisnienie"], hasData='true')
        return render_template("weather.html", title="Błąd", userForm=form,error='true')


    return render_template('weather.html', title="Strona głowna", userForm=form)


if __name__ == '__main__':
    app.run(debug=True)
