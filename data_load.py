from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "postgresql://david:pass234@localhost:5432/firedb"
db = SQLAlchemy(app)


# @dataclass
# class Address(db.Model):
#     __tablename__ = "Address"
#     id = db.Column(db.Integer, primary_key=True)
#     street = db.Column(db.String(120), nullable=False)
#     city = db.Column(db.String(120), nullable=False)
#     state = db.Column(db.String(2), nullable=False)
#     phone = db.Column(db.String(12), nullable=False)
#     website = db.Column(db.String(120), nullable=True)
#     facebook_link = db.Column(db.String(120), nullable=True)
#     image_link = db.Column(db.String(500), nullable=True)

#     def __repr__(self):
#         return f"<Address {self.id}: {self.street}, {self. city}, " \
#                f"{self.state}, {self.phone}>"


# artist_genres = db.Table("artist_genres", db.Column(
#     'artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
#     db.Column(
#     'genre_name', db.Integer, db.ForeignKey('Genre.name'), primary_key=True))


@dataclass
class Artist(db.Model):
    __tablename__ = "Artist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    street = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)

    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120), nullable=False, default="")
    genres = db.relationship("AristGenre")
    # genres = db.relationship("Genre", secondary=artist_genres,
    #                          backref=db.backref("artists", lazy=True))

    def __repr__(self):
        return f"<Artist {self.id}: {self.name}, " \
               f"{self.seeking_talent}, {self.seeking_description}>" \
               f"Address: {self.street}, {self. city}, " \
               f"{self.state}, {self.phone}>"


class ArtistGenre(db.Model):
    __tablename__ = "ArtistGenre"
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"))
    genre = db.Column(db.String(30), nullable=False)


# @dataclass
# class Genre(db.Model):
#     __tablename__ = "Genre"
#     # id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), primary_key=True)

#     def __repr__(self):
#         return f"<Genre {self.name}>"


db.create_all()


def init_load_addresses():
    address1 = Address(
        street="1015 Folsom Street",
        city="San Francisco",
        state="CA",
        phone="123-123-1234",
        website="https://www.themusicalhop.com",
        facebook_link="https://www.facebook.com/TheMusicalHop",
        image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    )
    address2 = Address(
        street="335 Delancey Street",
        city="New York",
        state="NY",
        phone="914-003-1132",
        website="https://www.theduelingpianos.com",
        facebook_link="https://www.facebook.com/theduelingpianos",
        image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"
    )
    address3 = Address(
        street="34 Whiskey Moore Ave",
        city="San Francisco",
        state="CA",
        phone="415-000-1234",
        website="https://www.parksquarelivemusicandcoffee.com",
        facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
    )
    addresses = [address1, address2, address3]
    for address in addresses:
        print(address)
        db.session.add(address)
        db.session.commit()


def init_load_genres():
    genres = [
        "Classical",
        "Folk",
        "Hip-Hop",
        "Jazz",
        "R&B",
        "Rock n Roll",
        "Reggae",
        "Swing"
    ]
    for genre in genres:
        print(Genre(name=genre))
        db.session.add(Genre(name=genre))
        db.session.commit()


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
