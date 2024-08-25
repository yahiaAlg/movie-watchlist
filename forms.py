from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, FloatField, PasswordField, SubmitField
from wtforms.validators import InputRequired, NumberRange, URL, DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea


class MovieForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    director = StringField("Director", validators=[InputRequired()])
    year = DateField("Year", format="%Y-%m-%d", validators=[InputRequired()])
    description = TextAreaField("Description", widget=TextArea())
    tags = StringField("Tags")
    casts = StringField("Casts")
    series = StringField("Series")
    rating = FloatField(
        "Rating", validators=[NumberRange(0, 10, "give a valid rating between 0:10")]
    )
    video_link = StringField("Video Link", validators=[
        URL()
    ])
    
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('Update Profile')