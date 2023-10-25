from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Events, Comment, Tickets
from .forms import EventsForm, CommentForm, TicketForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

evntbp = Blueprint('event', __name__, url_prefix='/events')

@evntbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Events).where(Events.id==id))
    comment_form = CommentForm()    
    purchase_form = TicketForm()
    return render_template('events/show.html', event=event, comment_form = comment_form, purchase_form = purchase_form)

@evntbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventsForm()
  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    event = Events(name=form.name.data, eventCategory=form.eventCategory.data, description=form.description.data, 
    image=db_file_path, ticketCapacity=form.ticketCapacity.data, ticketPrice=form.ticketPrice.data, 
    address1=form.address1.data, address2=form.address2.data, city=form.city.data, state=form.state.data, 
    postcode=form.postcode.data, venueCapacity=form.venueCapacity.data, eventDate=form.eventDate.data, eventTime=form.eventTime.data)
    db.session.add(event)
    db.session.commit()
    print('probably added to database')
    flash('Successfully created new Music Event', 'success')
    return redirect(url_for('event.create'))
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
      return redirect(url_for('event.show', id=event))
   return render_template('purchase.html', form=form)
