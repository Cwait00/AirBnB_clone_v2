#!/usr/bin/python3
"""starts a flask web application.
"""
from flask import Flask

app = Flask(__name__)

# Define the route for the root URL '/'
@app.route('/airbnb-onepage/', strict_slashes=False)
def hello():
    return "Hello HBNB!"

if __name__ == "__main__":
    # Start the flask development server
    # Listen on all available network interface (0.0.0.0) and port 5000
    app.run(host="0.0.0.0", port=5000)
