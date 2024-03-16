from flask import Blueprint, render_template, abort

home = Blueprint('home', __name__, tmeplate_folder='templates')


@home.route("/")
def home():
    return "home page"


def test():
    return 0

