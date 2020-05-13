from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from markupsafe import escape
from random import randint
from config import Config
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])   
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/login')
    return render_template('login.html',title = 'Sign In', form = form)

@app.route('/publications')
def pub_home():
    return render_template('pub_home.html')