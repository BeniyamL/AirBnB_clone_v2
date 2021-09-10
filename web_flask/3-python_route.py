#!/usr/bin/python3
""" a python script that starts a flask web application """


from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """ Display Hellow BNB """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def helo_hbnb():
    """ display HBNB """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_text(text):
    """ display c followed by the given text """
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python_text(text="is cool"):
    """ display python followed by the given text """
    text = text.replace("_", " ")
    return "Python {}".format(text)


if __name__ == "__main__":
    """ main method """
    app.run(host="0.0.0.0")
