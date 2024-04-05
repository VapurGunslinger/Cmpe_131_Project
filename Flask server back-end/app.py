from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from views import views

app = Flask(__name__, static_folder="static")
app.config['SQLACHEMY_DATABASE_URI']= 'sqlite:///animals.db'
# db= SQLAlchemy(app)







# class Appointment(db.module):
#     name= db.Column (db.String(100),nullable=False)
#     phoneNumber =db.Colomn(db.String(10), nullable=False)
    
#     #date_created= db.Colomn(db.DateTime, default datetime.utcnow)
#     def __repr__(self):
#         return '<Appointment %r>' % self.name #%self.appointment_date


##app.register_blueprint(views, url_prefix=("/"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Adoption_steps')
def adoption_steps():
    return render_template('Adoption_steps.html')

@app.route('/Animals')
def animals():
    return render_template('Animals.html')

@app.route('/Testimonial')
def testimonial():
    return render_template('Testimonials.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)