from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datatime import datatime

from views import views

app = Flask(__name__)
app.config['SQLACHEMY_DATABASE_URI']= 'sqlite:///test.db'

db= SQLAlchemy(app)

class Appointment(db.modle):
    name= db.Colomn (db.String(100),nullable=False)
    phoneNumber =db.Colomn(db.String(10), nullable=False)
    
    #date_created= db.Colomn(db.DateTime, default datetime.utcnow)
    def __repr__(self):
        return '<Appointment %r>' % self.name #%self.appointment_date

app.register_blueprint(views, url_prefix=("/"))

@app.route('/', methods= ['POST','GET'])
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)