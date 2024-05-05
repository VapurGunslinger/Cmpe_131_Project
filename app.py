from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Optional, NumberRange
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import logging
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
    # animal_id = db.Column(db.Integer, db.ForeignKey('animals.id',name='fk_appointment_animal', ondelete="CASCADE"))
    Appoint_DateTime = db.Column(db.DateTime)
    
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
    return render_template('apptschedule.html', animal = animal)

@app.route('/Animals/Schedule/Save', methods = ['POST'])
def schedule_save():
    form = request.form

    appoint_date_str = form['Appoint_Date']
    appoint_time_str = form['Appoint_Time_Slot']
    appoint_datetime = datetime.strptime(appoint_date_str + ' ' + appoint_time_str, '%Y-%m-%d %H:%M')

    appointment = Appointment(
        First_Name = form['First_Name'],
        Last_Name = form['Last_Name'],
        Email_Address = form['Email_Address'],
        Phone_Number = form['Phone_Number'],
        Appoint_DateTime=appoint_datetime,
        animal_id = form['animal_id']
    )
    db.session.add(appointment)
    db.session.commit()
    id=appointment.appt_id
    return redirect(url_for('appointmentsuccess', id=id))

@app.route('/Animals/Schedule/AppointmentSuccess/<int:id>')
def appointmentsuccess(id):
    appointment = Appointment.query.get_or_404(id)
    animal = Animal.query.get_or_404(appointment.animal_id)
    return render_template('success.html', appointment=appointment, animal=animal)


@app.route('/Adoption_steps')
def adoption_steps():
    return render_template('Adoption_steps.html')

# ADOPTABLE ANIMALS

@app.route('/Animals', methods=['GET', 'POST'])
def animals():
    all_animals = Animal.query.order_by(Animal.id.desc())
    return render_template('Animals.html', all_animals=all_animals)

@app.route('/Animals/<int:id>')
def animalpage(id):
    animal = Animal.query.get_or_404(id)
    return render_template('Animalpage.html', animal = animal)

# ADD, EDIT, DELETE ANIMALS
@app.route('/Animals/Add_Animal', methods=['GET', 'POST'])
def add_animal():
    name = None
    form = animalForm()

    if form.validate_on_submit():
        animal = Animal(name = form.name.data,
                        age = form.age.data,
                        species = form.species.data,
                        gender = form.gender.data,
                        breed = form.breed.data,
                        weight = form.weight.data,
                        description = form.description.data
                        )
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

@app.route('/Animals/Add_Animal/Delete/<int:id>')
def delete(id):
    animal_delete = Animal.query.get_or_404(id)
    related_appointments = Appointment.query.filter_by(animal_id=id).all()

    form = animalForm()
    try:
        for appointment in related_appointments:
            db.session.delete(appointment)
        db.session.delete(animal_delete)
        db.session.commit()
        flash("Animal and associated appointments deleted successfully.")
        return redirect("/Animals/Add_Animal")
    except:
        db.session.rollback()
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

@app.route('/Employee/Calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/api/appointments')
def get_appointments():
    appointments = Appointment.query.all()

    events = []
    for appt in appointments:
        # Use animal name as the event title
        animal = Animal.query.get(appt.animal_id)
        if animal is None:  # Check if animal is missing
            continue  # Skip this appointment if animal doesn't exist

        event = {
            "title": f"{animal.name}",
            "start": appt.Appoint_DateTime.isoformat(),  # ISO 8601 format
            "extendedProps": {
                "Booked by": "{} {}".format(appt.First_Name, appt.Last_Name),
                "Email": f"{appt.Email_Address}",
                "Phone": f"{appt.Phone_Number}"
            },

        }

        events.append(event)
    app.logger.info("Returned JSON: %s", events)
    return jsonify(events)  # Return the events as JSON

@app.route('/api/appointments/<date>')
def get_appointments_date(date):
    print(date)
    try:
        # Ensure the date is in the correct format
        date_obj = datetime.strptime(date, '%Y-%m-%d')  # Expected date format is 'YYYY-MM-DD'
    except ValueError:
        return jsonify({"error": "Invalid date format. Expected YYYY-MM-DD."}), 400
    appointments = Appointment.query.filter(
        db.func.date(Appointment.Appoint_DateTime) == date_obj.date()
    ).all()
    bookedtimes = []
    for appt in appointments:
        time_str = appt.Appoint_DateTime.strftime('%H:%M')
        bookedtimes.append(time_str)
    app.logger.info("Returned JSON: %s", bookedtimes)
    return jsonify(bookedtimes)  # Return the list of booked time slots
 
if __name__ == '__main__':
    app.run(debug=True, port=8000)