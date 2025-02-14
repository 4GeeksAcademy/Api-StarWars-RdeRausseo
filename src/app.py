"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/api/users', methods=['POST'])
def create_user():
    body = request.get_json()

    if not body.get('email') or not body.get('password'):
        return jsonify({"error": "Correo y contraseña obligatorios"}), 400

    existing_user = User.query.filter_by(email=body['email']).first()
    if existing_user:
        return jsonify({"error": "correo ya registrado"}), 400

    new_user = User(
        email=body['email'],
        password=body['password'],
        is_active=True  
    )

    
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@app.route('/api/planets', methods=['POST'])
def add_planet():
    body = request.get_json()
    if not body:
        return jsonify({"error": "body vacio"}), 400

    name = body.get('name')
    uid = body.get('uid')
    population = body.get('population')
    terrain = body.get('terrain')
    url = body.get('url')

    if not name or not uid:
        return jsonify({"error datos obligatorios:": "nombre y UID"}), 400

    new_planet = Planet(
        name=name,
        uid=uid,
        population=population,
        terrain=terrain,
        url=url
    )

    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201


@app.route('/api/characters', methods=['POST'])
def add_character():
    body = request.get_json()
    if not body:
        return jsonify({"error": "body vacio"}), 400

    name = body.get('name')
    uid = body.get('uid')
    gender = body.get('gender')
    url = body.get('url')

    if not name or not uid:
        return jsonify({"error datos obligatorios:": "nombre y UID"}), 400

    new_character = Character(
        name=name,
        uid=uid,
        gender=gender,
        url=url
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

@app.route('/api/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    return jsonify([personaje.serialize() for personaje in people]), 200

@app.route('/api/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Personaje no encontrdo"}), 404
    return jsonify(person.serialize()), 200

@app.route('/api/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planeta.serialize() for planeta in planets]), 200

@app.route('/api/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/api/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1  
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

@app.route('/api/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = 1  
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

@app.route('/api/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1  
    new_favorite = Favorite(user_id=user_id, character_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

@app.route('/api/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1  
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorito no encontrado"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "planeta eliminado con exito"}), 200

@app.route('/api/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1  
    favorite = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
    if not favorite:
        return jsonify({"error": "favorito no encontrdo"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "personaje eliminado con exito"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
