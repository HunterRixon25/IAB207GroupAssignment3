from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Events, User, Tickets
from . import db
from flask_login import current_user

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    event = db.session.scalars(db.select(Events)).all()
    bebop=Events.query.filter(Events.eventCategory.ilike('%Bebop%')).all()
    blues=Events.query.filter(Events.eventCategory.ilike('%Blues%')).all()
    soul=Events.query.filter(Events.eventCategory.ilike('%Soul%')).all()
    return render_template('index.html', event=event, bebop=bebop, blues=blues, soul=soul)


@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = request.args['search']
        search=Events.query.filter(Events.name.ilike('%' + query + '%') | Events.description.ilike('%' + query + '%') ).all()
        return render_template('search.html', search=search, query=query)
    else:
        return redirect(url_for('main.index'))
    
@mainbp.route('/myEvents')
def myEvents():
    myevents = Events.query.filter(Events.event_manager_id == current_user.id).all()
    if not myevents:
        flash('You have no events. Create one first!', 'danger')
        return redirect(url_for('main.index'))
    else:
        return render_template('myEvents.html', myevents=myevents)
    

@mainbp.route('/userBookingHistory')
def history():
    ticket = db.session.query(Events, Tickets).join(Events, Tickets.event_id == Events.id).filter(Tickets.user_id == current_user.id).all()
    if ticket:
        return render_template('userBookingHistory.html', ticket=ticket)
    else:
        flash('You have not purchased any tickets for events.', 'danger')
        return redirect(url_for('main.index'))

@mainbp.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@mainbp.errorhandler(400)
def bad_request(e):
    return render_template('400.html')

@mainbp.errorhandler(500)
def internal_error(e):
    return render_template('500.html')