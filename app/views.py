from flask import render_template, redirect, url_for, flash, session, Blueprint, current_app
from werkzeug.utils import secure_filename
from flask_login import login_required, login_user, logout_user
from . import db, login_manager
from .models import RunningWorkout, User
from .forms import AddRunForm, LoginForm, RegisterForm
from datetime import datetime
import os



main = Blueprint('main', __name__)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    form = LoginForm()
    if 'logged_in' not in session:
        return render_template('index.html', form=form)
    return redirect(url_for('main.profile'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Invalid email or password. Please try again', 'danger')
    return render_template('index.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        profile_picture_filename = None
        username = form.username.data
        email = form.email.data
        password = form.password.data
        profile_picture = form.profile_picture.data
        existing_email = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken. Please choose another one.', 'danger')
            return redirect(url_for('main.register'))
        if existing_email:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('main.login'))
        
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture_filename = f'{current_app.config["UPLOAD_FOLDER"]}/{filename}'
            profile_picture.save(profile_picture_filename)
            # Store only the relative path in the database
            profile_picture_filename = os.path.join('uploads', filename)
        

        user = User(username=username, email=email, profile_picture=profile_picture_filename)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)



@main.route('/add_run', methods=['GET', 'POST'])
@login_required
def add_run():
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    form = AddRunForm()
    if form.validate_on_submit():
        run = RunningWorkout(
            date=datetime.strptime(form.date.data, '%Y-%m-%d'),
            run_type = form.run_type.data,
            run_subtype = form.run_subtype.data,
        )

        if form.run_type.data == 'long_run':
            run.distance = form.distance.data
            run.duration = form.duration.data
            run.heart_rate = form.heart_rate.data
            run.calculate_average_pace()
        
        elif form.run_type.data == 'speed_run':
            if form.run_subtype.data == 'tempo':
                run.warmup_distance = form.warmup_distance.data
                run.main_part_distance = form.main_part_distance.data
                run.main_part_pace = form.main_part_pace.data
                run.heart_rate = form.heart_rate.data
                run.calculate_average_pace()
            elif form.run_subtype.data == 'intervals':
                run.run_structure = form.run_structure.data
                run.interval_details = form.interval_details.data
        
        db.session.add(run)
        db.session.commit()
        flash('Run added successfully!')
        return redirect(url_for('index'))
    return render_template('add_run.html', form=form)


@main.route('/profile')
@login_required
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = User.query.filter_by(id=session['user_id']).first()
    return render_template('profile.html', user_info=user.email, fitness_level="Current Fitness Level", next_goal="Next Goal")

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/training_plan')
@login_required
def view_training_plan():
    # Placeholder for the training plan data
    training_plan = [
        {"week": 1, "long_run": "5 km", "speed_workout": "Intervals: 4x400m"},
        {"week": 2, "long_run": "7 km", "speed_workout": "Tempo Run: 3 km at pace"},
        {"week": 3, "long_run": "8 km", "speed_workout": "Intervals: 5x400m"},
        # Add more weeks as needed
    ]
    
    return render_template('training_plan.html', training_plan=training_plan)