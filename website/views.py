from flask import Blueprint, render_template, request, redirect, url_for
from .models import Events
from . import db

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
        search=Events.query.filter(Events.name.ilike('%' + query + '%'))
        return render_template('search.html', search=search, query=query)
    else:
        return redirect(url_for('main.index'))

