#!/usr/bin/python3
""" a python script that starts a flask web application """


from flask import Flask, render_template


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


@app.route('/number/<int:n>', strict_slashes=False)
def display_number(n):
    """ display n is a number """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def display_template_number(n):
    """ display n is a number in rendering template if it is a number """
    return render_template("5-number.html", n=n)



if __name__ == "__main__":
    """ main method """
    app.run(host="0.0.0.0")
