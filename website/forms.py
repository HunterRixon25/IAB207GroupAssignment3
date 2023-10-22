from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, IntegerField, FloatField, TimeField, #DateField,
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

class EventsForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired()])
  eventCategory = StringField('Event Category', validators=[InputRequired()])
  description = TextAreaField('Description', 
            validators=[InputRequired()])
  image = FileField('Destination Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  ticketCapacity = StringField('Mumber of Tickets', validators=[InputRequired(), NumberRange(min=1)])
  ticketPrice = FloatField('Ticket Price', validators=[InputRequired()])
  address1 = StringField('Address 1', validators=[InputRequired()])
  address2 = StringField('Address 2')
  city = StringField('City', validators=[InputRequired()])
  state = SelectField('State', choices=[('', 'Select State'), ('Queensland', 'Queensland'), ('New South Wales', 'New South Wales'), ('Victoria', 'Victoria'), ('Western Australia', 'Western Australia'), ('South Australia', 'South Australia'), ('Tasmania', 'Tasmania')])
  postcode = StringField('Postcode', validators=[InputRequired()])
  venueCapacity = StringField('Total Venue Capacity', validators=[InputRequired(), NumberRange(min=1)])
  #eventDate = DateField('Event Date', format = '%d/%m/%Y', validators=[InputRequired()])
  eventTime = TimeField('Event Time', validators=[InputRequired()])
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
