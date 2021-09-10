#!/usr/bin/python3
""" a python script that starts a flask web application """


from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """ Display Hellow BNB """
    return "Hello HBNB!"


if __name__ == "__main__":
    """ main method """
    app.run(host="0.0.0.0")
