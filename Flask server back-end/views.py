from flask import Blueprint
from flask import Flask, render_template, url_for , request
# from flask_sqlalchemy import SQLAlchemy

views = Blueprint(__name__, "views")

@views.route('/')
def home():

    return render_template('home.html')


def test():
    return 0

