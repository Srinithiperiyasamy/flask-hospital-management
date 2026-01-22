from flask import Flask, render_template, redirect, url_for, request, abort
from flask_login import (
    LoginManager, login_user, login_required,
    logout_user, current_user
)
from flask_migrate import Migrate
from config import Config
from models import db, User, Doctor, Patient, Appointment, Billing

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "login"




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print("LOGIN ATTEMPT:", username, password)

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            print("LOGIN SUCCESS:", user.role)
            login_user(user)

            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user.role == "doctor":
                return redirect(url_for("doctor_dashboard"))
            elif user.role == "patient":
                return redirect(url_for("patient_dashboard"))

        print("LOGIN FAILED")

    return render_template("login.html")


@app.route("/admin")
@login_required
def admin_dashboard():
    return render_template("admin/dashboard.html")

@app.route("/admin/doctors")
@login_required
def admin_doctors():
    doctors = Doctor.query.all()
    print("DOCTORS:", doctors)  # 👈 DEBUG
    return render_template("admin/doctors.html", doctors=doctors)

@app.route("/admin/book/<int:doctor_id>", methods=["GET", "POST"])
@login_required
def book_appointment(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    patients = Patient.query.all()

    if request.method == "POST":
        appointment = Appointment(
            doctor_id=doctor.id,
            patient_id=request.form["user_id"],
            date=request.form["date"]
        )
        db.session.add(appointment)
        db.session.commit()
        return redirect(url_for("admin_doctors"))

    return render_template(
        "admin/book_appointment.html",
        doctor=doctor,
        patients=patients
    )

@app.route("/admin/patients")
@login_required
def admin_patients():
    if current_user.role != "admin":
        abort(403)

    appointments = Appointment.query.all()
    return render_template(
        "admin/patients.html",
        appointments=appointments
    )

@app.route('/patient/book', methods=['GET', 'POST'])
@login_required
def patient_book_appointment():
    if request.method == 'POST':
        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=request.form["doctor_id"],
            patient_name=request.form["patient_name"],
            patient_age=request.form["patient_age"],
            date=request.form["date"],
            time=request.form["time"],
            problem=request.form["problem"]
        )
        db.session.add(appointment)
        db.session.commit()

        # 👉 redirect to confirmation page
        return redirect(
            url_for('appointment_confirmed', appointment_id=appointment.id)
        )

    doctors = Doctor.query.all()
    return render_template("patient/book_appointment.html", doctors=doctors)

@app.route("/patient/appointment-confirmed/<int:appointment_id>")
@login_required
def appointment_confirmed(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    # Security: only owner can see it
    if appointment.patient_id != current_user.id:
        abort(403)

    return render_template(
        "patient/appointment_confirmed.html",
        appointment=appointment
    )




@app.route('/patient/appointments')
@login_required
def patient_appointments():
    appointments = current_user.appointments
    return render_template(
        "patient/appointments.html",
        appointments=appointments
    )

@app.route("/admin/appointments")
@login_required
def admin_appointments():
    if current_user.role != "admin":
        abort(403)

    appointments = Appointment.query.all()
    return render_template("admin/appointments.html", appointments=appointments)


@app.route("/admin/billing")
@login_required
def admin_billing():
    bills = Billing.query.all()
    return render_template("admin/billing.html", bills=bills)



@app.route("/doctor")
@login_required
def doctor_dashboard():
    return render_template("doctor/dashboard.html")

@app.route("/doctor/appointments", methods=["GET", "POST"])
@login_required
def doctor_appointments():
    if current_user.role != "doctor":
        abort(403)

    appointments = []

    if request.method == "POST":
        doctor_id = request.form.get("doctor_id")

        appointments = Appointment.query.filter_by(
            doctor_id=doctor_id
        ).all()

    return render_template(
        "doctor/appointments.html",
        appointments=appointments
    )



@app.route("/patient")
@login_required
def patient_dashboard():
    return render_template("patient/dashboard.html")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # ---- CREATE USERS (ONLY ONCE) ----
        if not User.query.first():
            db.session.add_all([
                User(username="admin", password="admin", role="admin"),
                User(username="doctor", password="doctor", role="doctor"),
                User(username="patient", password="patient", role="patient"),
            ])
            db.session.commit()



        # ---- CREATE DOCTORS (ONLY ONCE) ----
        if Doctor.query.count() == 0:
            doctors = [
                Doctor(name="Dr. John Smith", specialization="Cardiology", email="john.smith@example.com", phone="9876543210"),
                Doctor(name="Dr. Emily Davis", specialization="Dermatology", email="emily.davis@example.com", phone="9876543211"),
                Doctor(name="Dr. Michael Brown", specialization="Neurology", email="michael.brown@example.com", phone="9876543212"),
                Doctor(name="Dr. Sarah Wilson", specialization="Pediatrics", email="sarah.wilson@example.com", phone="9876543213"),
                Doctor(name="Dr. David Lee", specialization="Orthopedics", email="david.lee@example.com", phone="9876543214"),
                Doctor(name="Dr. Laura Martinez", specialization="Gynecology", email="laura.martinez@example.com", phone="9876543215"),
                Doctor(name="Dr. Robert Taylor", specialization="ENT", email="robert.taylor@example.com", phone="9876543216"),
                Doctor(name="Dr. Jessica Anderson", specialization="Ophthalmology", email="jessica.anderson@example.com", phone="9876543217"),
                Doctor(name="Dr. William Thomas", specialization="Urology", email="william.thomas@example.com", phone="9876543218"),
                Doctor(name="Dr. Olivia Jackson", specialization="Psychiatry", email="olivia.jackson@example.com", phone="9876543219"),
                Doctor(name="Dr. Daniel White", specialization="Cardiology", email="daniel.white@example.com", phone="9876543220"),
                Doctor(name="Dr. Sophia Harris", specialization="Dermatology", email="sophia.harris@example.com", phone="9876543221"),
                Doctor(name="Dr. James Martin", specialization="Neurology", email="james.martin@example.com", phone="9876543222"),
                Doctor(name="Dr. Isabella Thompson", specialization="Pediatrics", email="isabella.thompson@example.com", phone="9876543223"),
                Doctor(name="Dr. Benjamin Garcia", specialization="Orthopedics", email="benjamin.garcia@example.com", phone="9876543224"),
                Doctor(name="Dr. Mia Martinez", specialization="Gynecology", email="mia.martinez@example.com", phone="9876543225"),
                Doctor(name="Dr. Alexander Robinson", specialization="ENT", email="alex.robinson@example.com", phone="9876543226"),
                Doctor(name="Dr. Charlotte Clark", specialization="Ophthalmology", email="charlotte.clark@example.com", phone="9876543227"),
                Doctor(name="Dr. Henry Lewis", specialization="Urology", email="henry.lewis@example.com", phone="9876543228"),
                Doctor(name="Dr. Amelia Walker", specialization="Psychiatry", email="amelia.walker@example.com", phone="9876543229"),
            ]
            db.session.add_all(doctors)
            db.session.commit()


    app.run(debug=True)
