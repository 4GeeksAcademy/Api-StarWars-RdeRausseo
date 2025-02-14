from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(250), unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(100))
    terrain = db.Column(db.String(100))
    url = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "url": self.url,
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(250), unique=True, nullable=False)  
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250))
    url = db.Column(db.String(250)) 

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "gender": self.gender,
            "url": self.url,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)

    def __repr__(self):
        return f'<Favorite user_id={self.user_id} planet_id={self.planet_id} character_id={self.character_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
        }