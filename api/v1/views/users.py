#!/usr/bin/python3
"""User"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User

@app_views.route('/users',methods=['GET'])
def get_users():
    users = storage.get(User).values()
    if users is None:
        abort(404)

    dict_users = []
    for user in users:
        dict_users.append(user.to_dict())
    return jsonify(dict_users)


@app_views.route('/users/<user_id>', methods=["GET"])
def get_user_id(user_id):
    """Retrieves a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object with id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()

    return jsonify({}), 200


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def post_user():
    """Creates a user"""
    user = request.get_json()

    if user is None:
        abort(400, "Not a JSON")
    if 'email' not in user:
        abort(400, 'Missing email')
    if 'password' not in user:
        abort(400, 'Missing password')

    body = User(**user)
    storage.new(body)
    storage.save()

    return jsonify(body.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_city(user_id):
    """Updates a State object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        request_htpp = request.get_json()
        if request_htpp is None:
            abort(400, 'Not a JSON')

    for key, value in request_htpp.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()

    return jsonify(user.to_dict()), 200
