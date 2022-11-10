from flask import Flask, render_template

app =Flask(__name__)

@app.route('/')
def index():
    return render_template('weather.html', title="Strona głowna")

@app.route('/user/<name>')
def user(name):
    return render_template('weather.html', title="Uzytkownik", name=name)

if __name__ == '__main__':
    app.run()