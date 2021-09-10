#!/usr/bin/python3
""" a python script that starts a flask web application """


from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route('/states', strict_slashes=False)
def display_all_state():
    """ Display all states """
    all_state = storage.all("State")
    return render_template("7-states_list.html", all_state=all_state)


@app.route('/states/<id>', strict_slashes=False)
def display_state(id):
    """ Display the given state by id """
    state = storage.all("State").values()
    for st in state:
        if st.id == id:
    	    return render_template("9-states.html", state=st)
    return render_template("9-states.html")


@app.teardown_appcontext
def close_SQLAlchemy(exc):
    """ remove the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    """ main method """
    app.run(host="0.0.0.0")
