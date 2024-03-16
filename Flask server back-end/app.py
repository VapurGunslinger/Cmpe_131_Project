from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from views import views

app = Flask(__name__)

app.register_blueprint(views, url_prefix=("/"))

if __name__ == '__main__':
    app.run(debug=True, port=8000)