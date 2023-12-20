#!/usr/bin/python3

'''
A module that contains a route for app_views.
'''

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})


def get_stats():
    """retrieves the number of each object"""

    stats = {
        storage.count('Amenities'),
        storage.count('City'),
        storage.count('Place'),
        storage.count('Review'),
        storage.count('State'),
        storage.count('user'),
    }

    return jsonify(stats)
