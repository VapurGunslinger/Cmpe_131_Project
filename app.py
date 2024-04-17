from flask import Flask, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Optional, NumberRange

# from werkzeug.utils import secure_filename
# import uuid as uuid
# import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shelter.db'
app.config['SECRET_KEY'] = "shelterkey"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    species = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.Integer, nullable=False)

    breed = db.Column(db.String(150), nullable=True)
    weight = db.Column(db.Numeric, nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(300), nullable=True)
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
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Appointment %r>' % self.name 

# app.register_blueprint(views, url_prefix=("/"))

# Forms
class animalForm(FlaskForm):
    name = StringField("Animal Name: ", validators=[DataRequired()])
    age = IntegerField("Age: ", validators=[Optional(), NumberRange(min=0, message = "Input must be greater than 0.")])
    species = SelectField(u"Species: ",  choices=[(0, 'Cat'),(1, 'Dog')], validators=[DataRequired()])
    gender = SelectField(u"Gender: ", choices=[(0, 'Male'),(1, 'Female'), (2, 'Neutered'), (3, 'Spayed')], validators=[DataRequired(),] )
    submit = SubmitField("Submit")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Adoption_steps')
def adoption_steps():
    return render_template('Adoption_steps.html')

@app.route('/Animals', methods=['GET', 'POST'])
def animals():
    all_animals = Animal.query.order_by(Animal.id.desc())
    return render_template('Animals.html', all_animals=all_animals)

@app.route('/Animals/Add_Animal', methods=['GET', 'POST'])
def add_animal():
    name = None
    age = None
    species = None
    gender = None
    form = animalForm()

    if form.validate_on_submit():
        animal = Animal(name = form.name.data,
                        age = form.age.data,
                        species = form.species.data,
                        gender = form.gender.data)
        db.session.add(animal)
        db.session.commit()
        name = form.name.data
        age = form.age.data
        species = form.species.data
        gender = form.gender.data
        #clear data
        flash(name + " was added successfully!")
        form = animalForm(formdata=None)
    all_animals = Animal.query.order_by(Animal.id)
    return render_template('add_animal.html',  
        form = form,
        all_animals=all_animals)

@app.route('/Animals/<int:id>')
def animalpage(id):
    animal = Animal.query.get_or_404(id)
    return render_template('Animalpage.html', animal = animal)

@app.route('/Animals/Add_Animal/Delete/<int:id>')
def delete(id):
    animal_delete = Animal.query.get_or_404(id)
    form = animalForm()
    try:
        db.session.delete(animal_delete)
        db.session.commit()
        flash("Animal deleted successfully.")

        all_animals = Animal.query.order_by(Animal.id)
        return render_template('add_animal.html',  
            form = form,
            all_animals=all_animals)
    except:
        flash("Unable to delete the animal from the database.")
        all_animals = Animal.query.order_by(Animal.id)
        return render_template('add_animal.html',  
            form = form,
            all_animals=all_animals)

@app.route('/Testimonial')
def testimonial():
    return render_template('Testimonials.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)