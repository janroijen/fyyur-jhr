from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "postgresql://david:pass234@localhost:5432/firedb"
db = SQLAlchemy(app)

show = db.Table('show',
                db.Column('artist_id', db.Integer,
                          db.ForeignKey('Artist.id'), primary_key=True),
                db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'),
                          primary_key=True),
                db.Column('start_time', db.DateTime, nullable=False))


@dataclass
class Artist(db.Model):
    __tablename__ = "Artist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)

    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120), nullable=False, default="")
    genres = db.relationship("ArtistGenre", backref="artist")
    venues = db.relationship("Venue", secondary=show, back_populates="artists")

    def __repr__(self):
        return f"<Artist {self.id}: {self.name}, " \
               f"{self.seeking_talent}, {self.seeking_description}\n" \
               f" Address: {self.street}, {self. city}, " \
               f"{self.state}, {self.phone}>"


class ArtistGenre(db.Model):
    __tablename__ = "ArtistGenre"
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"))
    genre = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"<ArtistGenre {self.id}: {self.artist}, {self.genre}"


class Venue(db.Model):
    __tablename__ = "Venue"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)

    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120), nullable=False, default="")
    genres = db.relationship("VenueGenre", backref="venue")
    artists = db.relationship("Artist", secondary=show, back_populates="venues")

    def __repr__(self):
        return f"<Venue {self.id}: {self.name}, " \
               f"{self.seeking_talent}, {self.seeking_description}\n" \
               f" Address: {self.street}, {self. city}, " \
               f"{self.state}, {self.phone}>"


class VenueGenre(db.Model):
    __tablename__ = "VenueGenre"
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"))
    genre = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"<VenueGenre {self.id}: {self.artist}, {self.genre}"


def init_load_artists():
    artist1 = Artist(
      name="Guns N Petals",
      genres=[ArtistGenre(genre="Rock n Roll")],
      city="San Francisco",
      state="CA",
      phone="326-123-5000",
      website="https://www.gunsnpetalsband.com",
      facebook_link="https://www.facebook.com/GunsNPetals",
      seeking_venue=True,
      seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
      image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    )

    artist2 = Artist(
      name="Matt Quevedo",
      genres=[ArtistGenre(genre="Jazz")],
      city="New York",
      state="NY",
      phone="300-400-5000",
      facebook_link="https://www.facebook.com/mattquevedo923251523",
      seeking_venue=False,
      image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
    )

    artist3 = Artist(
      name="The Wild Sax Band",
      genres=[ArtistGenre(genre="Jazz"), ArtistGenre(genre="Classical")],
      city="San Francisco",
      state="CA",
      phone="432-325-5432",
      seeking_venue=False,
      image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
    )

    db.session.add_all([artist1, artist2, artist3])
    db.session.commit()


def init_load_venues():
    venue1 = Venue(
        name="The Musical Hop",
        genres=[VenueGenre(genre="Jazz"), VenueGenre(genre="Reggae"), VenueGenre(genre="Swing"), VenueGenre(genre="Classical"), VenueGenre(genre="Folk")],
        address="1015 Folsom Street",
        city="San Francisco",
        state="CA",
        phone="123-123-1234",
        website="https://www.themusicalhop.com",
        facebook_link="https://www.facebook.com/TheMusicalHop",
        image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        seeking_talent=True,
        seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us."
    )

    venue2 = Venue(
        name="The Dueling Pianos Bar",
        genres=[VenueGenre(genre="Classical"), VenueGenre(genre="R&B"), VenueGenre(genre="Hip-Hop")],
        address="335 Delancey Street",
        city="New York",
        state="NY",
        phone="914-003-1132",
        website="https://www.theduelingpianos.com",
        facebook_link="https://www.facebook.com/theduelingpianos",
        image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        seeking_talent=False
    )

    venue3 = Venue(
        name="Park Square Live Music & Coffee",
        genres=[VenueGenre(genre="Rock n Roll"), VenueGenre(genre="Jazz"), VenueGenre(genre="Classical"), VenueGenre(genre="Folk")],
        address="34 Whiskey Moore Ave",
        city="San Francisco",
        state="CA",
        phone="415-000-1234",
        website="https://www.parksquarelivemusicandcoffee.com",
        facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        seeking_talent=False
    )

    db.session.add_all([venue1, venue2, venue3])
    db.session.commit()


db.drop_all()
db.create_all()
init_load_artists()
init_load_venues()


# init_load_addresses()
# init_load_genres()


# @app.route("/addresses")
# def get_addresswa():
#     addresses = Address.query.all()
#     print(addresses)
#     return jsonify([x.__repr__() for x in addresses])


# @app.route("/address/<address_id>")
# def get_address(address_id):
#     address = Address.query.filter_by(id=address_id).first()
#     print(address)
#     return jsonify(address.__repr__())


@app.route("/")
def index():
    return "Hello World!"
