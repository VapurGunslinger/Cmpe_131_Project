from flask import Flask, render_template, url_for , request
from flask_sqlalchemy import SQLAlchemy
#from datatime import datatime

from views import views

app = Flask(__name__)
# app.config['SQLACHEMY_DATABASE_URI']= 'sqlite:///test.db'
# db= SQLAlchemy(app)

# class Appointment(db.modle):
#     name= db.Colomn (db.String(100),nullable=False)
#     phoneNumber =db.Colomn(db.String(10), nullable=False)
    
#     #date_created= db.Colomn(db.DateTime, default datetime.utcnow)
#     def __repr__(self):
#         return '<Appointment %r>' % self.name #%self.appointment_date

# #employ side claander fill here.

# app.register_blueprint(views, url_prefix=("/"))

# @app.route('/')
# def index():
#     # return "Hello World!"
#     return render_template('Home.html')
@app.route('/')
@app.route('/home')
def home_page():
    print("was here")
    return render_template('Home.html')

# @app.route('/adoption Steps')
# def adoption_steps():
#     return render_template('adotion_steps.html',item_name ='phone')






if __name__ == '__main__':
    app.run(debug=True, port=8000)