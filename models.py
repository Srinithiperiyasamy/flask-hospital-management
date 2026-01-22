from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    role = db.Column(db.String(20))


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))



class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))



class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))
    patient_name = db.Column(db.String(100))  # add this
    patient_age = db.Column(db.Integer)       # add this
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    problem = db.Column(db.String(200))

    patient = db.relationship("User", backref="appointments", lazy=True)
      # patient points to User

    doctor = db.relationship("Doctor", backref="appointments", lazy=True)


class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"))
    amount = db.Column(db.Float)
    status = db.Column(db.String(20))
