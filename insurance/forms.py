from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, SubmitField, BooleanField,\
                     DecimalField, IntegerField, FieldList, FormField, Form
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from wtforms.fields.html5 import DateField
from insurance.models import Customer, Driver, Vehicle
from flask_login import current_user

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    marital_status = SelectField('Marital Status', 
                    choices=[('M', 'Married'), ('S', 'Single'), ('W', 'Widow/Widower')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    comfirm_password = PasswordField('Comfirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')
    
    # check if email exists
    def validate_email(self, email):
        customer = Customer.query.filter_by(email=email.data).first()
        if customer:
            raise ValidationError('That email has been taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') 
    
class UpdateAccountForm(FlaskForm):
    marital_status = SelectField('Marital Status', 
                    choices=[('M', 'Married'), ('S', 'Single'), ('W', 'Widow/Widower')])
    address = StringField('Address', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    # check if email exists
    def validate_email(self, email):
        if email.data != current_user.email:
            user = Customer.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email has been taken. Please choose a different one.')
 
class SelectInsuranceForm(FlaskForm):
    insurance_type = SelectMultipleField('Insurance Type', 
                                        choices=[('A', 'Auto'), ('H', 'Home')])
    submit = SubmitField('Next')

class DriverForm(Form):
    # sub-subform
    license_number = StringField('Driver’s license number', validators=[DataRequired(), Length(min=9, max=9)])
    driver_name = StringField('Driver’s Name', validators=[DataRequired()])
    birthdate = DateField('Birthdate', format='%Y-%m-%d', validators=[DataRequired()]) 
    
    # check if pk exists
    def validate_license_number(self, license_number):
        driver = Driver.query.filter_by(license_number=license_number.data).first()
        if driver:
            raise ValidationError('This driver exists. Please enter another one.') 
 
class VehicleForm(FlaskForm):
    # Subform1
    vin = StringField('Vehicle VIN', validators=[DataRequired(), Length(min=17, max=17)])
    make_model_year = IntegerField('Vehicle make-model-year', validators=[DataRequired(), NumberRange(min=1800, max=2020)])
    status = SelectField('Status', choices=[('L', 'Leased'), ('F', 'Financed'), ('O', 'Owned')])  
    
    drivers = FieldList(
        FormField(DriverForm),
        min_entries=1
    ) 
    
    # check if pk exists
    def validate_vin(self, vin):
        vehicle = Vehicle.query.filter_by(vin=vin.data).first()
        if vehicle:
            raise ValidationError('This vehicle exists. Please add another one.') 
    
class AutoForm(FlaskForm):
    # Parent Form
    vehicles = FieldList(
        FormField(VehicleForm),
        min_entries=1
    )
    # TODO: add an installation check
    #1 TODO: add a duration choice(90 days, half year, one year...)
    submit = SubmitField('Start 90-day Auto Insurance!')  

class HouseForm(Form):
    # Subform
    purchase_date = DateField('Purchase date', format='%Y-%m-%d', validators=[DataRequired()])
    purchase_value = DecimalField('Purchase value', validators=[DataRequired()])
    home_area = DecimalField('Home area in Sq. Ft', validators=[DataRequired()])
    home_type = SelectField('Type', choices=[('S', 'Single family'), ('M', 'Multi Family'), ('C', 'Condominium'), ('T', 'Town house')])   
    # Four Parameters
    fire = BooleanField('Auto Fire Notification')
    security = BooleanField('Home Security System')
    swimming_pool = SelectField('Swimming Pool', choices=[('U', 'Underground'), ('O', 'Overground'), ('I', 'Indoor'), ('M', 'Multiple'), ('N', 'None')])
    basement = BooleanField('Basement')
    
class HomeForm(FlaskForm):
    # Parent Form
    houses = FieldList(
        FormField(HouseForm),
        min_entries=1
    )
    
    submit = SubmitField('Start 90-day Home Insurance!')
    
class PaymentForm(FlaskForm):
    
    method = SelectField('Payment method', choices=[('P', 'PayPal'), ('C', 'Credit'), ('D', 'Debit'), ('K', 'Check')])   
    submit = SubmitField('Pay now!')