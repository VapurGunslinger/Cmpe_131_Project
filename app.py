from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Optional, NumberRange
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shelter.db'
app.config['SECRET_KEY'] = "shelterkey"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

ANIMAL_IMAGE_FOLDER = "static/animal_images/"
app.config['UPLOAD_FOLDER'] = ANIMAL_IMAGE_FOLDER 

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    species = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)

    breed = db.Column(db.String(150), nullable=True)
    weight = db.Column(db.Numeric, nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
            return '<Name %r>' % self.name

class Appointment(db.Model):
    __tablename__ = 'appointments'
    appt_id = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String(100),nullable=False)
    Last_Name = db.Column(db.String(100),nullable=False)
    Email_Address = db.Column(db.String(100),nullable=False)
    Phone_Number = db.Column(db.String(10), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))
    Appoint_Date = db.Column(db.DateTime)
    Appoint_Time = db.Column(db.DateTime)
    
    def __repr__(self):
        return '<Appointment %r>' % self.name 

# app.register_blueprint(views, url_prefix=("/"))

# Forms
class animalForm(FlaskForm):
    name = StringField("Animal Name: ", validators=[DataRequired()])
    age = IntegerField("Age: ", validators=[DataRequired(), NumberRange(min=0, message = "Input must be greater than 0.")])
    species = SelectField(u"Species: ",  choices=[(0, 'Cat'),(1, 'Dog')], validators=[DataRequired()])
    gender = SelectField(u"Gender: ", choices=[(0, 'Male'),(1, 'Female'), (2, 'Neutered Male'), (3, 'Spayed Female')], validators=[DataRequired(),] )
    
    breed = StringField("Breed: ", validators=[Optional()])
    weight = DecimalField("Weight (lbs): ", validators=[Optional()])
    description = TextAreaField('Description: ', [validators.optional(), validators.length(max=800)])
    image = FileField("Animal image: ")
    submit = SubmitField("Submit")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Animals/Schedule/<int:id>')
def schedule(id):
    animal = Animal.query.get_or_404(id)
    return render_template('calendar.html', animal = animal)

@app.route('/Animals/Schedule/Save', methods = ['POST'])
def schedule_save():
    form = request.form

    appoint_date_str = form['Appoint_Date']
    appoint_time_str = form['Appoint_Time']
    appoint_datetime = datetime.strptime(appoint_date_str + ' ' + appoint_time_str, '%Y-%m-%d %H:%M')

    appointement = Appointment(
        First_Name = form['First_Name'],
        Last_Name = form['Last_Name'],
        Email_Address = form['Email_Address'],
        Phone_Number = form['Phone_Number'],
        # Appoint_Date = form['Appoint_Date'],
        # Appoint_Time = form['Appoint_Time'],
        Appoint_Date=appoint_datetime,
    )
    db.session.add(appointement)
    db.session.commit()
    return "Successfully submitted"

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
        name = form.name.data
        # Save image
        if request.files.get("image"):
            animal.image_path = request.files['image']
            image_filename = secure_filename(animal.image_path.filename)
            image_uniquename = str(uuid.uuid1()) + "_" + image_filename
            saver = request.files['image']
            animal.image_path = image_uniquename
            try:
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], image_uniquename))
                db.session.commit()
                flash(name + " was added successfully!")
                form = animalForm(formdata=None)
            except:
                flash("Error adding " + name + " to database.")
        else:
            try:
                db.session.commit()
                flash(name + " was added successfully!")
                form = animalForm(formdata=None)
            except:
                flash("Error adding " + name + " to database.")
            
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
        return redirect("/Animals/Add_Animal")
    except:
        flash("Unable to delete the animal from the database.")
        return redirect("/Animals/Add_Animal")
    
@app.route('/Animals/Add_Animal/Update/<int:id>', methods=['GET','POST']) 
def update(id):
    animal_update = Animal.query.get_or_404(id)
    form = animalForm(obj=animal_update)
    if request.method == "POST":
        form.populate_obj(animal_update)
        name = form.name.data
        if request.files.get("image"):
            animal_update.image_path = request.files['image']
            image_filename = secure_filename(animal_update.image_path.filename)
            image_uniquename = str(uuid.uuid1()) + "_" + image_filename
            saver = request.files['image']
            animal_update.image_path = image_uniquename
            try:
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], image_uniquename))
                db.session.commit()
                flash(name + " was updated successfully!")
                return redirect(url_for('update', id=id))
            except:
                flash("Error adding to database.")
                return redirect(url_for('update', id=id))
        else:
            try:
                db.session.commit()
                flash(name + " updated successfully!")
                return redirect(url_for('update', id=id))
            except:
                flash("Error with updating animal.")
                return redirect(url_for('update', id=id))
    else:
       return render_template("update.html", form=form, animal_update=animal_update)



@app.route('/Testimonial')
def testimonial():
    return render_template('Testimonials.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)