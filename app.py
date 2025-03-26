from flask import Flask, redirect, render_template, request, url_for
from helpers import db_get_stations, db_get_trains

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    trains = db_get_trains()
    stations = db_get_stations()

    if request.method == "POST":
        selected_train = request.form.get("train")
        selected_station = request.form.get("station")
        return redirect(url_for("stats", train=selected_train, station=selected_station))

    return render_template("index.html", stations=stations, trains=trains)


@app.route("/stats")
def stats():
    train = request.args.get("train")
    station = request.args.get("station")

    # Placeholder for stats calculation
    statistics = {
        "average_delay": "5 min",
        "on_time_percentage": "87%",
        "total_arrivals": 120
    }

    return render_template("stats.html", train=train, station=station, statistics=statistics)

if __name__ == '__main__':
    app.run(debug=True)
