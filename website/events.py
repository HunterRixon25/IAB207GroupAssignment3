from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Events, EventState, Comment, Tickets
from .forms import EventsForm, CommentForm, TicketForm, EditForm
from . import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

evntbp = Blueprint('event', __name__, url_prefix='/events')

# Self explainatory
def update_event_state():
   now = datetime.now()
   events = Events.query.all()

   for event in events: 
      if event.eventDate <= now.date():
         if event.eventTime <= now.time():
            event.eventState = EventState.EXPIRED.value
      elif event.ticketsSold == event.ticketCapacity:
         event.eventState = EventState.SOLD.value

   db.session.commit()

@evntbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Events).where(Events.id==id))
    comment_form = CommentForm()    
    purchase_form = TicketForm()

    update_event_state() # check to see if events can be updated yet.

    genre_events = db.session.query(Events).filter(Events.eventCategory == event.eventCategory, Events.id != event.id).all()

    return render_template('events/show.html', event=event, comment_form = comment_form, purchase_form = purchase_form, genre_events = genre_events)

@evntbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventsForm()
    if form.validate_on_submit():
      now = datetime.now()

      # Check if the datetime the user has entered is valid.
      if form.eventDate.data < now.date():
         if form.eventTime.data < now.time():
            flash('The date/time you have entered is invalid!', 'danger')
            return redirect(url_for('event.create'))
      
      # Check if the entered venue capacity & ticket capacity values are valid
      if form.venueCapacity.data < form.ticketCapacity.data:
         flash('Venue Capacity cannot be smaller than number of tickets!', 'danger')
         return redirect(url_for('event.create'))

      db_file_path = check_upload_file(form)
      event = Events(name=form.name.data, event_manager_id=current_user.id, eventCategory=form.eventCategory.data, description=form.description.data, 
      image=db_file_path, ticketCapacity=form.ticketCapacity.data, ticketPrice=form.ticketPrice.data, 
      address1=form.address1.data, address2=form.address2.data, city=form.city.data, state=form.state.data, 
      postcode=form.postcode.data, venueCapacity=form.venueCapacity.data, eventDate=form.eventDate.data, eventTime=form.eventTime.data, eventState=EventState.OPEN.value)
      db.session.add(event)
      db.session.commit()
      print('probably added to database')
      flash('Successfully created new Music Event', 'success')
      return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=form)

def check_upload_file(form):
  fp = form.image.data
  filename = fp.filename 
  BASE_PATH = os.path.dirname(__file__)

  # Ensure the directory exists
  upload_directory = os.path.join(BASE_PATH, 'static', 'img')
  
  upload_path = os.path.join(upload_directory, secure_filename(filename))
  db_upload_path = '/static/img/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path

@evntbp.route('/<event>/comment', methods=['GET', 'POST'])  
@login_required
def comment(event):  
    update_event_state() # Check to see if event states can be updated.
    form = CommentForm()  
    event_obj = Events.query.filter_by(id=event).first()
    if form.validate_on_submit():  
      comment = Comment(text=form.text.data, 
                        events_id=event_obj.id,
                        user_id=current_user.id) 
      db.session.add(comment) 
      db.session.commit() 

      #flash('Your comment has been added', 'success')  
    return redirect(url_for('event.show', id=event))

@evntbp.route('/<event>/purchase', methods=['GET', 'POST'])
@login_required
def purchase(event):
   form = TicketForm()
   event_obj = Events.query.filter_by(id=event).first()
   if form.validate_on_submit():
      if form.ticketsPurchased.data > (event_obj.ticketCapacity - event_obj.ticketsSold):
        flash("Not enough tickets avalaible.")
        return redirect(url_for('event.show', id=event))
      for _ in range(int(form.ticketsPurchased.data)):
          ticket = Tickets(event_id=event_obj.id, user_id=current_user.id)
          db.session.add(ticket)
      flash("Ticket id: " + str(ticket.id) + " successfully purchased!")
      # Subtract the number of tickets avaliable from event
      event_obj.ticketsSold += form.ticketsPurchased.data
          
      db.session.commit()
          
      flash(f"Successfully purchased {str(form.ticketsPurchased.data)} tickets!")

      update_event_state() # Check to see if events can be updated now.

      return redirect(url_for('event.show', id=event))
   return render_template('purchase.html', form=form)
         
@evntbp.route('/<event>/edit', methods=['GET', 'POST'])
@login_required
def edit(event):
    event_obj = Events.query.filter_by(id=event).first()

    if not event_obj:
       flash('Event not found!', 'danger')
       return redirect(url_for('main.index'))

    #Ensure the current user is the one who created the event. 
    if event_obj.event_manager_id != current_user.id:
      flash('You do not have permission to edit this event.', 'danger')
      return redirect(url_for('main.index'))
   
    # Pre-populate the form with the event's original details
    form = EditForm()
    if request.method == 'GET':
      form.name.data = event_obj.name
      form.eventCategory.data = event_obj.eventCategory
      form.description.data = event_obj.description
      form.ticketCapacity.data = event_obj.ticketCapacity
      form.ticketPrice.data = event_obj.ticketPrice
      form.address1.data = event_obj.address1
      form.address2.data = event_obj.address2
      form.city.data = event_obj.city
      form.state.data = event_obj.state
      form.postcode.data = event_obj.postcode
      form.venueCapacity.data = event_obj.venueCapacity
      form.eventDate.data = event_obj.eventDate
      form.eventTime.data = event_obj.eventTime

    if form.validate_on_submit():
        now = datetime.now()

        # Check if the datetime the user has entered is valid.
        if form.eventDate.data < now.date():
          if form.eventTime.data < now.time():
            flash('The date/time you have entered is invalid!', 'danger')
            return redirect(url_for('main.index'))
      
        # Check if the entered venue capacity & ticket capacity values are valid
        if form.venueCapacity.data < form.ticketCapacity.data:
          flash('Venue Capacity cannot be smaller than number of tickets!', 'danger')
          return redirect(url_for('main.index'))
        
        # Attempt to catch a very sneaky potential error
        if event_obj.ticketsSold > form.ticketCapacity.data:
          flash('Attempt to push invalid data', 'danger')
          return redirect(url_for('main.index'))

        db_file_path = check_upload_file_edit(form)
        if not db_file_path:
           db_file_path = event_obj.image
        
        # Update the event's data
        event_obj.name = form.name.data
        event_obj.eventCategory = form.eventCategory.data
        event_obj.eventState = form.cancelEvent.data
        event_obj.description = form.description.data
        event_obj.image = db_file_path
        event_obj.ticketCapacity = form.ticketCapacity.data
        event_obj.ticketPrice = form.ticketPrice.data
        event_obj.address1 = form.address1.data
        event_obj.address2 = form.address2.data
        event_obj.city = form.city.data
        event_obj.state = form.state.data
        event_obj.postcode = form.postcode.data
        event_obj.venueCapacity = form.venueCapacity.data
        event_obj.eventDate = form.eventDate.data
        event_obj.eventTime = form.eventTime.data

        db.session.commit()

        update_event_state() # Check to see if event states can be updated.

        return redirect(url_for('event.show', id=event))
    else:
       print(form.errors)
    return render_template('events/edit.html', form=form)

def check_upload_file_edit(form):
  fp = form.image.data

  # Check if no file was uploaded
  if not fp:
     return None
  
  filename = fp.filename 
  BASE_PATH = os.path.dirname(__file__)

  # Ensure the directory exists
  upload_directory = os.path.join(BASE_PATH, 'static', 'img')
  
  upload_path = os.path.join(upload_directory, secure_filename(filename))
  db_upload_path = '/static/img/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path
