#!/usr/bin/python3
"""
a script that starts a Flask web application
"""


from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

@app.teardown_appcontext
def teardown_appcontext(self):
    '''
    a method to handle @app.teardown_appcontext
    '''
    storage.close()

if __name__ == "__main__":
    app.run(host=os.environ.get('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.environ.get('HBNB_API_PORT', 5000)),
            threaded=True)
