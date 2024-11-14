from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash= db.Column(db.String(120), nullable=False)
    profile_picture = db.Column(db.String(120), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)





class RunningWorkout(db.Model):
    __tablename__ = 'running_workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    run_type = db.Column(db.String(50), nullable=False)
    run_subtype = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False) # in Minutes
    distance = db.Column(db.Float, nullable=False) # in Km
    average_pace = db.Column(db.Float, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)

    # fields specific for a Tempo run
    warmup_distance = db.Column(db.Float, nullable=True)
    main_part_distance = db.Column(db.Float, nullable=True)
    main_part_pace = db.Column(db.Float, nullable=True)

    # fields specific for a Interval run
    run_structure = db.Column(db.String(50), nullable=True)
    interval_details = db.Column(db.String(50), nullable=True)

    def calculate_average_pace(self):
        if self.distance and self.duration:
            minutes_per_km = self.distance / self.duration
            self.average_pace = f"{int(minutes_per_km)}:{int((minutes_per_km % 1) * 60):02d} min/km"
    