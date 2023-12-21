#!/usr/bin/python3
"""City"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.state import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    States = storage.get(State, state_id)
    dict_json = []
    for city in States.cities:
        dict_json.append(city.to_dict())
    return jsonify(dict_json)


@app_views.route('/cities/city_id', methods=["GET"])
def get_city_id(city_id):
    """Retrieves a State object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/states/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a State object with id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def post_city(state_id):
    """Creates a city"""
    state = storage.get(State, state_id)

    city = request.get_json()
    if city is None:
        abort(400, "Not a JSON")

    if "name" not in city:
        abort(400, "Missing name")

    body = City(state_id=state_id, **city)
    storage.new(body)
    storage.save()

    return jsonify(body.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Updates a State object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        request_htpp = request.get_json()
        if request_htpp is None:
            abort(400, 'Not a JSON')

    for key, value in request_htpp.items():
        if key not in ['id', 'state_id' ,'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()

    return jsonify(city.to_dict()), 200
