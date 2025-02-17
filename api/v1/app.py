#!/usr/bin/python3
"""
a script that starts a Flask web application
"""

from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_views)

# Enable CORS for all routes under "/api/v1/"
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    '''
    a method to handle @app.teardown_appcontext
    '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """not found"""
    return jsonify(error="Not found"), 404

if __name__ == "__main__":
    app.run(host=os.environ.get('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.environ.get('HBNB_API_PORT', 5000)),
            threaded=True)
