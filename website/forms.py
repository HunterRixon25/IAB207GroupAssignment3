from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeLocalField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

class EventsForm(FlaskForm):
  name = StringField('Name', validators=[InputRequired()])
  eventCategory = StringField('Event Category', validators=[InputRequired()])
  description = TextAreaField('Description', 
            validators=[InputRequired()])
  image = FileField('Destination Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  tickets = StringField('Tickets', validators=[InputRequired()])
  ticketType = StringField('Ticket Type', validators=[InputRequired()])
  ticketPrice = StringField('Ticket Price', validators=[InputRequired()])
  eventLink = StringField('Event Link', validators=[InputRequired()])
  address1 = StringField('Address 1', validators=[InputRequired()])
  address2 = StringField('Address 2')
  city = StringField('City', validators=[InputRequired()])
  state = StringField('State', validators=[InputRequired()])
  postcode = StringField('Postcode', validators=[InputRequired()])
  venueCapacity = StringField('Venue Capacity', validators=[InputRequired()])
  eventTags = StringField('Event Tags', validators=[InputRequired()])
  eventDateTime = DateTimeLocalField('Event Date and Time', format = '%d/%m/%YT%H:%M', validators=[InputRequired()])
  submit = SubmitField("Create")
    
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')