from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, ValidationError,Email, EqualTo,Length
from app.models import User


class LoginForm(FlaskForm):
    task_1 = StringField('Հեռախոսահամար', validators=[DataRequired()])
    task_2 = PasswordField('Հասցե', validators=[DataRequired()])
    task_3 = PasswordField('Մթերք', validators=[DataRequired()])
    submit_1 = SubmitField('Պատվիրել')

    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить пароль')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    lastname = StringField('Фамиля', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('пароль')])
    submit = SubmitField('Регистрация')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
