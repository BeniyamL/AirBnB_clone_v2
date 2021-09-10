#!/usr/bin/python3
""" a python script that starts a flask web application """


from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/cities_by_states', strict_slashes=False)
def index():
    """ Display all states """
    all_state = storage.all("State")
    return render_template("8-cities_by_states.html", all_state=all_state)


@app.teardown_appcontext
def close_SQLAlchemy(exc):
    """ remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    """ main method """
    app.run(host="0.0.0.0")
