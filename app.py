from datetime import datetime, timedelta

import duckdb
from flask import Flask, redirect, render_template, request, url_for

from helpers import db_get_stations, db_get_trains, find_station_id, get_average_time

app = Flask(__name__)
DB_PATH = "db/uusikaupunki.duckdb"

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

    if not train or not station:
        return redirect(url_for("index", error="Invalid request. Please select a train and a station."))

    station_id = find_station_id(station)
    if station_id is None:
        return redirect(url_for("index", error=f"Station '{station}' not found."))

    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    with duckdb.connect(DB_PATH) as con:
        arrivals_df = con.execute(
            """
            SELECT arrival_time FROM train_arrivals 
            WHERE train_id = ? AND station_id = ? AND arrival_time >= ?
            """,
            [train, station_id, start_date]
        ).pl()

    if arrivals_df.is_empty():
        return render_template("stats.html", train=train, station=station, avg_time=None, error="No data found.")

    avg_arrival_time = get_average_time(arrivals_df, "arrival_time")

    return render_template("stats.html", train=train, station=station, avg_time=avg_arrival_time, error=None)

if __name__ == '__main__':
    app.run(debug=True)
