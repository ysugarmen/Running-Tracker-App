from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateField, TextAreaField, SubmitField, FloatField, PasswordField, FileField
from wtforms.validators import DataRequired, Optional, Email, EqualTo








class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    profile_picture = FileField('Profile Picture')  # Optional, if uploading profile pictures
    submit = SubmitField('Register')


class AddRunForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    run_type = SelectField(
        'Running type',
        choices = [('long_run', 'Long Run'), ('speed_run', 'Speed Run')],
        validators=[DataRequired()]
    )
    run_subtype = SelectField(
        'Running subtype',
        choices = [('tempo', 'Tempo'), ('intervals', 'Intervals')],
        validators=[Optional()]
    )

    # Fields for Long Run
    distance = IntegerField('Distance (km)', validators=[Optional()])
    duration = StringField('Duration (Minutes)', validators=[Optional()])
    heart_rate = IntegerField('Average Heart Rate (bpm)', validators=[Optional()])

    # Fields for Tempo Run
    warmup_distance = FloatField('Warmup Distance (km)', validators=[Optional()])
    main_distance = FloatField('Main Distance (km)', validators=[Optional()])
    main_pace = StringField('Main Part Pace (min/km)', validators=[Optional()])

    # Fields for Intervals Run
    run_structure = StringField('Run Structure', validators=[Optional()])
    interval_details = TextAreaField('Interval Details', validators=[Optional()])

    submit = SubmitField('Add Run')