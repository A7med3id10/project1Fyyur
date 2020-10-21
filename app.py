import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# DONE: connect to a local postgresql database

# Models.


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone}>'


# DONE: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    concert = db.relationship("Shows", backref="party")

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration

class Shows(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    start_time = db.Column(db.String())
    artist = db.relationship("Artist", backref="artist_here")
    venue = db.relationship("Venue", backref="some_venue")

# Filters.


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

# Controllers.


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues


@app.route('/venues')
def venues():
    # DONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = Venue.query.all()
    return render_template('pages/venues.html', areas=data, venues=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    srch = str(search_term)
    response = Venue.query.filter(Venue.name.ilike('%'+srch+'%'))
    return render_template('pages/search_venues.html', results=response.count(), response=Venue.query.filter(Venue.name.ilike('%'+srch+'%')), search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    data = Venue.query.get(venue_id)
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # DONE: insert form data as a new Venue record in the db, instead
    # DONE: modify data to be the data object returned from db insertion
    # on successful db insert, flash success
    # DONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    # DONE: populate form with fields from artist with ID <artist_id>
    error = False
    body = {}
    try:
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        facebook_link = request.form.get('facebook_link')
        new_venue = Venue(name=name, city=city, state=state,
                          address=address, phone=phone, facebook_link=facebook_link)
        db.session.add(new_venue)
        db.session.commit()
        body['name'] = new_venue.name
        body['city'] = new_venue.city
        body['state'] = new_venue.state
        body['address'] = new_venue.address
        body['phone'] = new_venue.phone
        body['facebook_link'] = new_venue.facebook_link
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
        flash('An error occurred. Venue ' +
              data.name + ' could not be listed.')
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')


@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
    # DONE: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    try:
        unNeededVEN = Venue.query.get(venue_id)
        db.session.delete(unNeededVEN)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    # return None

#  Artists


@app.route('/artists')
def artists():
    # DONE: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    srch = str(search_term)
    response = Artist.query.filter(Artist.name.ilike('%'+srch+'%'))
    return render_template('pages/search_venues.html', results=response.count(), response=Artist.query.filter(Artist.name.ilike('%'+srch+'%')), search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    data = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    # DONE: populate form with fields from artist with ID <artist_id>
    neededArtist = Artist.query.get(artist_id)
    neededArtist.name = form.name
    neededArtist.city = form.city
    neededArtist.state = form.state
    neededArtist.phone = form.phone
    neededArtist.genres = form.genres
    neededArtist.facebook_link = form.facebook_link
    return render_template('forms/edit_artist.html', form=form, artist=neededArtist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # DONE: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    updatedArtist = Artist.query.get(artist_id)
    error = False
    try:
      _name = request.form.get('name')
      _city = request.form.get('city')
      _state = request.form.get('state') 
      _phone = request.form.get('phone')
      _genres = request.form.get('genres')
      _facebook_link = request.form.get('facebook_link')
      edit = Artist.query.get(artist_id)
      edit.name = _name
      edit.city = _city
      edit.state = _state
      edit.phone = _phone
      edit.genres = _genres
      edit.facebook_link = _facebook_link
      db.session.commit()
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    # DONE: populate form with values from venue with ID <venue_id>
    neededVenue = Venue.query.get(venue_id)
    neededVenue.name = form.name
    neededVenue.city = form.city
    neededVenue.state = form.state
    neededVenue.phone = form.phone
    neededVenue.genres = form.genres
    neededVenue.facebook_link = form.facebook_link
    return render_template('forms/edit_venue.html', form=form, venue=neededVenue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    _name = request.form.get('name')
    _city = request.form.get('city')
    _state = request.form.get('state') 
    _phone = request.form.get('phone')
    _address = request.form.get('address')
    _genres = request.form.get('genres')
    _facebook_link = request.form.get('facebook_link')
    edit = Venue.query.get(venue_id)
    edit.name = _name
    edit.city = _city
    edit.state = _state
    edit.phone = _phone
    edit.address = _address
    edit.genres = _genres
    edit.facebook_link = _facebook_link
    db.session.commit()
  except():
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(500)
  else:
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # DONE: insert form data as a new Venue record in the db, instead
    # DONE: modify data to be the data object returned from db insertion
    # on successful db insert, flash success
    # DONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    error = False
    body = {}
    try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone')
      genres = request.form.get('phone')
      facebook_link = request.form.get('facebook_link')
      new_artist = Artist(name=name, city=city, state=state, genres=genres, phone=phone, facebook_link=facebook_link)
      db.session.add(new_artist)
      db.session.commit()
      body['name'] = new_artist.name
      body['city'] = new_artist.city
      body['state'] = new_artist.state
      body['genres'] = new_artist.genres
      body['phone'] = new_artist.phone
      body['facebook_link'] = new_artist.facebook_link
    except():
      db.session.rollback()
      error = True
      print(sys.exc_info())
      flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    finally:
      db.session.close()
    if error:
      abort(500)
    else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      return render_template('pages/home.html')

#  Shows

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # DONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = Shows.query.all()
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # DONE: insert form data as a new Show record in the db, instead
    # on successful db insert, flash success
    # DONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    error = False
    body = {}
    try:
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get('start_time')
      new_show = Shows(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      db.session.add(new_show)
      db.session.commit()
      body['artist_id'] = new_show.artist_id
      body['venue_id'] = new_show.venue_id
      body['start_time'] = new_show.start_time
    except():
      db.session.rollback()
      error = True
      print(sys.exc_info())
      flash('An error occurred. Show could not be listed.')
    finally:
      db.session.close()
    if error:
      abort(500)
    else:
      flash('Show was successfully listed!')
      return render_template('pages/home.html')


# FINISHED........


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# Launch.

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
