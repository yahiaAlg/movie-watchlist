from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, FloatField
from wtforms.validators import InputRequired, NumberRange, URL
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
    
