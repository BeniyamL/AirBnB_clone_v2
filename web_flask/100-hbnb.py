#!/usr/bin/python3
""" a python script that starts a flask web application """


from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """ Display content of hbnb """
    all_states = storage.all("State")
    all_amenities = storage.all("Amenity")
    all_places = storage.all("Place")
    return render_template("100-hbnb.html", all_states=all_states,
                           all_amenities=all_amenities, all_places=all_places)


@app.teardown_appcontext
def close_SQLAlchemy(exc):
    """ remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    """ main method """
    app.run(host="0.0.0.0")
