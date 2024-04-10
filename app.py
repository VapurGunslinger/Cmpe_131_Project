from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///shelter.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    species = db.Column(db.String(150), nullable=False)
    breed = db.Column(db.String(150), nullable=False)
    weight = db.Column(db.Numeric, nullable=False)
    gender = db.Column(db.Integer, nullable=False)
    decription = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(300))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
            return '<Name %r>' % self.name

class Appointment(db.Model):
    __tablename__ = 'appointments'
    appt_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    phoneNumber = db.Column(db.String(10), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))
    date = db.Column(db.DateTime)
   # date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Appointment %r>' % self.name 


# app.register_blueprint(views, url_prefix=("/"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Adoption_steps')
def adoption_steps():
    return render_template('Adoption_steps.html')

@app.route('/Animals')
def animals():
    return render_template('Animals.html')

# @app.route('/Animals/<int:id>')
# def animals():
#     animal = Animal.query.get_or_404(id)
#     return render_template('Animalpage.html', animal = animal)

@app.route('/Testimonial')
def testimonial():
    return render_template('Testimonials.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)