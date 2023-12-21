#!/usr/bin/python3
"""State"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    Amenities = storage.all(Amenity)
    dict_json = []
    for amenities in Amenities.values():
        dict_json.append(amenities.to_dict())
    return jsonify(dict_json)


@app_views.route('/amenities/<amenity_id>', methods=["GET"])
def get_amenities_id(amenity_id):
    """Retrieves a State object"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    else:
        return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a State object with id"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    else:
        storage.delete(amenities)
        storage.save()

    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenities():
    """Creates a State"""
    body = request.get_json()

    if body is None:
        abort(400, "Not a JSON")

    if "name" not in body:
        abort(400, "Missing name")

    amenities = Amenity(**body)
    storage.new(amenities)
    storage.save()

    return jsonify(amenities.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenities(amenity_id):
    """Updates a State object"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    else:
        request_htpp = request.get_json()
        if request_htpp is None:
            abort(400, 'Not a JSON')

    for key, value in request_htpp.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenities, key, value)

    storage.save()

    return jsonify(amenities.to_dict()), 200
