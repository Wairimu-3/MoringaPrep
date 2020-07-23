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

    tutorial_heading = StringField('Travel Blog Title', validators=[Required()])
    tutorial_content = TextAreaField('Blog contents', validators=[Required()])
    tutorial_author = StringField('Blog Author', validators=[Required()])
    submit = SubmitField('Submit')

