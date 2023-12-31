from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, IntegerField, FloatField, DateField, TimeField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange, Regexp, Length, DataRequired
from flask_wtf.file import FileRequired, FileField, FileAllowed
from .models import EventState

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

class EventsForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired()])
  # eventCategory = StringField('Event Category', validators=[InputRequired()])
  eventCategory = SelectField('Event Category', choices=[('', 'Select Category'), ('Blues', 'Blues'), ('Bebop', 'Bebop'), ('Soul', 'Soul')])
  description = TextAreaField('Description', 
            validators=[InputRequired()])
  image = FileField('Destination Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  ticketCapacity = IntegerField('Number of Tickets', validators=[InputRequired(), NumberRange(min=1)])
  ticketPrice = FloatField('Ticket Price', validators=[InputRequired()])
  address1 = StringField('Address 1', validators=[InputRequired()])
  address2 = StringField('Address 2')
  city = StringField('City', validators=[InputRequired()])
  state = SelectField('State', choices=[('', 'Select State'), ('Queensland', 'Queensland'), ('New South Wales', 'New South Wales'), ('Victoria', 'Victoria'), ('Western Australia', 'Western Australia'), ('South Australia', 'South Australia'), ('Tasmania', 'Tasmania')])
  postcode = StringField('Postcode', validators=[InputRequired()])
  venueCapacity = IntegerField('Total Venue Capacity', validators=[InputRequired(), NumberRange(min=1)])
  eventDate = DateField('Event Date', validators=[InputRequired()])
  eventTime = TimeField('Event Time', validators=[InputRequired()])
  submit = SubmitField("Create Event")

class EditForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired()])
  # eventCategory = StringField('Event Category', validators=[InputRequired()])
  eventCategory = SelectField('Event Category', choices=[('', 'Select Category'), ('Blues', 'Blues'), ('Bebop', 'Bebop'), ('Soul', 'Soul')])
  cancelEvent = SelectField('Change Event Status', choices=[(EventState.OPEN.value, EventState.OPEN.value), (EventState.CANCELLED.value, EventState.CANCELLED.value)])
  description = TextAreaField('Description', 
            validators=[InputRequired()])
  image = FileField('Destination Image', validators=[
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  ticketCapacity = IntegerField('Number of Tickets', validators=[InputRequired(), NumberRange(min=1)])
  ticketPrice = FloatField('Ticket Price', validators=[InputRequired()])
  address1 = StringField('Address 1', validators=[InputRequired()])
  address2 = StringField('Address 2')
  city = StringField('City', validators=[InputRequired()])
  state = SelectField('State', choices=[('', 'Select State'), ('Queensland', 'Queensland'), ('New South Wales', 'New South Wales'), ('Victoria', 'Victoria'), ('Western Australia', 'Western Australia'), ('South Australia', 'South Australia'), ('Tasmania', 'Tasmania')])
  postcode = StringField('Postcode', validators=[InputRequired()])
  venueCapacity = IntegerField('Total Venue Capacity', validators=[InputRequired(), NumberRange(min=1)])
  eventDate = DateField('Event Date', validators=[InputRequired()])
  eventTime = TimeField('Event Time', validators=[InputRequired()])
  submit = SubmitField("Update Event")
    
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone = StringField('Phone No.',validators=[DataRequired(),Regexp(regex=r'^(?:\+?(61))? ?(?:\((?=.*\)))?(0?[2-57-8])\)? ?(\d\d(?:[- ](?=\d{3})|(?!\d\d[- ]?\d[- ]))\d\d[- ]?\d[- ]?\d{3})$')]) #This regex captures any australian phone number, that's all you need to know.
    postcode = StringField("Post Code (Address)", validators=[InputRequired("Please provide your home's post code."), Length(min=4, max=4)])
    
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')

class TicketForm(FlaskForm):
   ticketsPurchased = IntegerField('Tickets purchased', validators=[InputRequired(), NumberRange(min=1)])
   submit = SubmitField('Purchase')
