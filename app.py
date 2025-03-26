from flask import Flask, redirect, render_template, request, url_for
from helpers import get_stations, get_trains

app = Flask(__name__)


@app.route("/")
def index():
    trains = get_trains()
    stations = get_stations()
    return render_template("index.html", stations=stations, trains=trains)


if __name__ == '__main__':
    app.run(debug=True)
