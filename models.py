from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from typing import List
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "postgresql://david:pass234@localhost:5432/firedb"
db = SQLAlchemy(app)


class Artist(db.Model):
    __tablename__ = "Artist"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(), nullable=False)

    city: str = db.Column(db.String(120), nullable=False)
    state: str = db.Column(db.String(2), nullable=False)
    phone: str = db.Column(db.String(12), nullable=False)
    website: str = db.Column(db.String(120), nullable=True)
    facebook_link: str = db.Column(db.String(120), nullable=True)
    image_link: str = db.Column(db.String(500), nullable=True)

    seeking_venue: bool = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description: str = db.Column(db.String(120), nullable=False,
                                         default="")
    genres: List[str] = db.relationship("ArtistGenre", backref="artist")
    venues: List[str] = db.relationship("Show", back_populates="artist")

    def __repr__(self):
        return f"<Artist {self.id}: {self.name}, " \
               f"{self.seeking_venue}, {self.seeking_description}\n" \
               f" Address: {self.city}, {self.state}, {self.phone}>"


class ArtistGenre(db.Model):
    __tablename__ = "ArtistGenre"
    id: int = db.Column(db.Integer, primary_key=True)
    artist_id: int = db.Column(db.Integer, db.ForeignKey("Artist.id"))
    genre: int = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"<ArtistGenre {self.id}: {self.artist}, {self.genre}"


class Venue(db.Model):
    __tablename__ = "Venue"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(), nullable=False)

    address: str = db.Column(db.String(120), nullable=False)
    city: str = db.Column(db.String(120), nullable=False)
    state: str = db.Column(db.String(2), nullable=False)
    phone: str = db.Column(db.String(12), nullable=False)
    website: str = db.Column(db.String(120), nullable=True)
    facebook_link: str = db.Column(db.String(120), nullable=True)
    image_link: str = db.Column(db.String(500), nullable=True)

    seeking_talent: bool = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description: str = db.Column(db.String(120), nullable=False,
                                         default="")
    genres: List[str] = db.relationship("VenueGenre", backref="venue")
    artists: List[str] = db.relationship("Show", back_populates="venue")

    def __repr__(self):
        return f"<Venue {self.id}: {self.name}, " \
               f"{self.seeking_talent}, {self.seeking_description}\n" \
               f" Address: {self.street}, {self. city}, " \
               f"{self.state}, {self.phone}>"


class VenueGenre(db.Model):
    __tablename__ = "VenueGenre"
    id: int = db.Column(db.Integer, primary_key=True)
    venue_id: int = db.Column(db.Integer, db.ForeignKey("Venue.id"))
    genre: str = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"<VenueGenre {self.id}: {self.venue}, {self.genre}"


class Show(db.Model):
    __tablename__ = "Show"
    id: int = db.Column(db.Integer, primary_key=True)
    artist_id: int = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    artist: str = db.relationship(
        'Artist', backref=db.backref('shows', cascade='all, delete'))
    venue_id: int = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'), nullable=False)
    venue: str = db.relationship(
        'Venue', backref=db.backref('shows', cascade='all, delete'))
    start_time: datetime = db.Column(db.DateTime(), nullable=False)


def init_load():
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

    show1 = Show(artist=artist1, venue=venue1,
                 start_time="2019-05-21T21:30:00.000Z")
    show2 = Show(artist=artist2, venue=venue3,
                 start_time="2019-06-15T23:00:00.000Z")
    show3 = Show(artist=artist3, venue=venue3,
                 start_time="2035-04-01T20:00:00.000Z")
    show4 = Show(artist=artist3, venue=venue3,
                 start_time="2035-04-08T20:00:00.000Z")
    show5 = Show(artist=artist3, venue=venue3,
                 start_time="2035-04-15T20:00:00.000Z")

    db.session.add_all([show1, show2, show3, show4, show5])
    db.session.commit()


# set-up tables and load initial data
if __name__ == "main":
    db.drop_all()
    db.create_all()
    init_load()
