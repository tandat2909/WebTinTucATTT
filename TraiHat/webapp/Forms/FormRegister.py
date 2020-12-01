from flask_wtf import FlaskForm,Form
from wtforms import StringField, PasswordField, SelectField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

GENDER_LIST = {
    ('None', 'None'),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Oder', 'Oder'),

}


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password ', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    pseudonym = StringField('Pseudonym', validators=[DataRequired()])
    gender = SelectField('Gender', choices=GENDER_LIST)
    phone_number = StringField('Phone number')
    address = StringField('Address')

    def get_gender(self):
        choice = dict(self.gender.choices).get(self.gender.data, "")
        return choice
    def get_dict(self):
        data ={
            'username': self.username.data,
            'email': self.email.data,
            'password': self.password.data,
            'firstname': self.firstname.data,
            'lastname': self.lastname.data,
            'pseudonym': self.pseudonym.data,
            'phone_number': self.phone_number.data,
            'address': self.address.data,
            'gender': self.get_gender()
        }
        return data

