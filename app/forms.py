from flask_wtf import FlaskForm
import wtforms as wf
from wtforms import validators
from app.models import User, Employee


class EmployeeForm(FlaskForm):
    fullname = wf.StringField(label='ФИО', validators=[validators.DataRequired()])
    phone = wf.IntegerField(label='Номер телефона', validators=[validators.DataRequired()])
    short_info = wf.TextAreaField(label='Информация', validators=[validators.DataRequired()])
    experience = wf.IntegerField(label='Опыт работы', validators=[validators.DataRequired()])
    preferred_position = wf.StringField(label='Желаемая должность в компании')
    submit = wf.SubmitField(label='Подтвердить')


    def validate_fullname(self, name):
        s = ' '
        if s not in name.data:
            raise validators.ValidationError('Необходимо ввести фамилию вместе с именем')


class UserForm(FlaskForm):
    username = wf.StringField(label='Имя пользоватля', validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=64)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        validators.DataRequired(),
        validators.Length(min=8, max=64)
    ])
    submit = wf.SubmitField(label='Подтвердить')
