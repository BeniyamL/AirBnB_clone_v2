#!/usr/bin/python3
""" a python script that starts a flask web application """


from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/hbnb_filters', strict_slashes=False)
def display_hbnb():
    """ Display all states """
    all_states = storage.all("State")
    all_amenities = storage.all("Amenity")
    return render_template("10-hbnb_filters.html",
                           all_states=all_states, all_amenities=all_amenities)


@app.teardown_appcontext
def close_SQLAlchemy(exc):
    """ remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    """ main method """
    app.run(host="0.0.0.0")
