#!/usr/bin/python3
"""State api"""


from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve the list of all State objects"""
    States = storage.all(State)
    dict_json = []
    for state in States.values():
        dict_json.append(state.to_dict())
    return jsonify(dict_json)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_id(state_id):
    """Retreive a state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """Del a state by ID"""
    state_del = storage.get(State, state_id)
    if state_del is None:
        abort(404)

    storage.delete(state_del)
    storage.save()

    return jsonify({}), 200

@app_views.route('/states', methods='POST', strict_slashes=False)
def create_state():
    """Create a new State object"""
    data = request.get_json()
    if not data:
        abort(400, "not a JSON")
    if 'name' not in data:
        abort(400)

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods='PUT', strict_slashes=False)
def update_state(state_id):
    """Update state by ID"""
    up_state = storage.get(State, state_id)
    if up_state is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'update_at']:
            setattr(up_state, key, value)

    up_state.save()
    return jsonify(up_state.to_dict()), 200
