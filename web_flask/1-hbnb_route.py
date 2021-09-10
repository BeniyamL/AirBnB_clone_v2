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
def disply_text(text):
    """ display C followed by the value of a text """
    text = text.replace("_", " ")
    return "C {}".format(text)

if __name__ == "__main__":
    """ main method """
    app.run(host="0.0.0.0")
