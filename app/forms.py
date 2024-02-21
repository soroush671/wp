from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import re


class LoginForm(FlaskForm):
    username = StringField('نام کاربری',  validators=[DataRequired()])
    password = StringField('رمز عبور')
    remember_me = BooleanField('مرا به خاطر بسپار')
    submit = SubmitField('تایید')
    add = SubmitField('افزودن به سبد')
    quantity = StringField('')# def validate_phone_number(self, phone_number):
    #     mobile_regex = "^09(1[0-9]|3[0-9]|0[0-9])-?[0-9]{3}-?[0-9]{4}$"
    #     if not (re.search(mobile_regex, phone_number.data)):
    #         raise ValidationError('شماره موبایل به درستی وارد نشده است')
    #
