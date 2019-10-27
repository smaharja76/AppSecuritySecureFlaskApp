from flask import Flask
from flask_wtf import FlaskForm
from flask import render_template, request, escape
from wtforms import StringField, PasswordField, validators
from flask_wtf.csrf import CSRFProtect
import os

#csrf = CSRFProtect()
app = Flask(__name__)
#app.config['WTF_CSRF_ENABLED'] = True
csrf = CSRFProtect()
csrf.init_app(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
#app.config['WTF_CSRF_CHECK_DEFAULT'] =False
#keep track of registered users
registered = {}
loggedin = {}

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=50, message=(u'username must be between 4 and 25 chars long')), validators.DataRequired()], id='uname')
    password = PasswordField('Password', [validators.Length(min=4, max=25), validators.DataRequired()], id='pword')
    twofactor = StringField('2-factor phone', [validators.Length(min=4,max=15), validators.DataRequired()], id='2fa')

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25, message=(u'username must be between 4 and 25 chars long')), validators.DataRequired()], id='uname')
    password = PasswordField('Password', [validators.Length(min=4, max=25), validators.DataRequired()], id='pword')
    twofactor = StringField('2-factor phone', [validators.Length(min=4,max=15), validators.DataRequired()], id='2fa')


class SpellCheckForm(FlaskForm):
    words = StringField('Enter words', [validators.Length(min=1), validators.DataRequired()], id='inputtext')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = escape(form.username.data)
        phone = escape(form.twofactor.data)
        if(user in registered and registered[user]['password'] == escape(form.password.data)):
            if registered[user]['phone'] == phone:   
                loggedin[user]=True
                return render_template('login_success.html')
            else:
                return '<html><h1 id="result"> Two-factor authentication failure!</h1> <form method="post"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/></form></html>'
        else:
            return '<html><h1 id="result">Incorrect username or password!</h1> <form method="post"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/></form></html>'

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = form.username.data
        if user in registered:
            return render_template('register_fail.html')
        registered[user] = {"password":escape(form.password.data), "phone":escape(form.twofactor.data)}
        return render_template('register_success.html')
    return render_template('register.html', form=form)


@app.route('/spell_check', methods=['GET','POST'])
def spell_check():
    form = SpellCheckForm(request.form)
    if request.method == 'POST' and form.validate():
        return render_template('spell_check_result.html')
    return render_template('spell_check.html', form=form)
