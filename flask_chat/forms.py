''' forms for the app '''

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_chat.models import User, Channel, Messege

class RegForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirmed_password = PasswordField('confirmed_password',
    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('signup')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("that username is taken, please choose another")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("that email is taken, please choose another")


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember Me')
    submit = SubmitField('login')


class ImgUploadForm(FlaskForm):
    image = FileField('update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class CreateChannelForm(FlaskForm):
    chname = StringField('chname', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('submit')

    def validate_chname(self, chname):
        channel = Channel.query.filter_by(title=chname.data).first()
        user = User.query.filter_by(username=chname.data).first()
        if channel:
            raise ValidationError("this name is already taken")
        elif user:
            raise ValidationError("this name is already taken")


class CreateMessegeForm(FlaskForm):
    send_txt = StringField('msg', validators=[DataRequired()])
    submit = SubmitField('Send Message')