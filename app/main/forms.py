from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    details = TextAreaField('Enter your comments', validators=[Required()])
    submit = SubmitField('Submit')

class TutorialForm(FlaskForm):

    tutorial_heading = StringField('Tutorial Title', validators=[Required()])
    tutorial_content = TextAreaField('Tutorial content', validators=[Required()])
    tutorial_author = StringField('Written by:', validators=[Required()])
    submit = SubmitField('Submit')

