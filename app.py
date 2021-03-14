# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, abort, render_template, request, Response
from flask import flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from forms import VenueForm, ArtistForm, ShowForm
from flask_migrate import Migrate
from models import Show, Artist, Venue

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    try:
        data = Venue.byLocation()
        return render_template('pages/venues.html', areas=data)
    except DBAPIError:
        return render_template('errors/500.html')


@app.route('/venues/search', methods=['POST'])
def search_venues():
    try:
        response = Venue.search(request.form.get("search_term"))
        return render_template('pages/search_venues.html', results=response,
                               search_term=request.form.get('search_term', ''))
    except DBAPIError:
        return render_template("errors/500.html")


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    try:
        data = Venue.query.get(venue_id).details
        return render_template('pages/show_venue.html', venue=data)
    except AttributeError:
        return abort(404)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    try:
        venue = Venue.create(form)
        flash('Venue ' + venue.name + ' was successfully listed!')
    except (DBAPIError, SQLAlchemyError):
        flash('An error occurred. Venue ' +
              request.form["name"] + ' could not be listed.')

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.delete(venue_id)
    except (DBAPIError, SQLAlchemyError):
        abort(404)

    return Response(status=200)

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    try:
        response = Artist.search(request.form.get("search_term"))
        return render_template('pages/search_artists.html', results=response,
                               search_term=request.form.get('search_term', ''))
    except DBAPIError:
        return render_template("errors/500.html")


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    try:
        data = Artist.query.get(artist_id).details
        return render_template('pages/show_artist.html', artist=data)
    except AttributeError:
        return abort(404)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.find(artist_id)
    if artist is None:
        return abort(404)
    else:
        form = ArtistForm(data=artist)
        return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    Artist.update(artist_id, form)
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.find(venue_id)
    if venue is None:
        return abort(404)
    else:
        form = VenueForm(data=venue)
        return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form)
    Venue.update(venue_id, form)
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)
    try:
        artist = Artist.create(form)
        flash('Artist ' + artist.name + ' was successfully listed!')
    except (DBAPIError, SQLAlchemyError):
        flash('An error occurred. Artist ' +
              request.form["name"] + ' could not be listed.')

    return render_template('pages/home.html')


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        Artist.delete(artist_id)
    except (DBAPIError, SQLAlchemyError):
        abort(404)

    return Response(status=200)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    try:
        data = [show.details for show in Show.query.all()]
        return render_template('pages/shows.html', shows=data)
    except AttributeError:
        return abort(404)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show form
    form = ShowForm(request.form)
    try:
        venue_id = form.venue_id.data
        artist_id = form.artist_id.data
        start_time = form.start_time.data

        show = Show(venue_id=venue_id, artist_id=artist_id,
                    start_time=start_time)
        db.session.add(show)
        db.session.commit()

        flash('Show was successfully listed!')
    except DBAPIError:
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
