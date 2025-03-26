from datetime import datetime, timedelta
import duckdb
from flask import Flask, redirect, render_template, request, url_for
from helpers import db_get_stations, db_get_trains, find_station_id, plot_accumulated_arrivals

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
    station_id = find_station_id(station)
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    with duckdb.connect("db/uusikaupunki.duckdb") as con:
        arrivals_df = con.execute(f"""
            SELECT arrival_time FROM train_arrivals
            WHERE train_id = {train} AND station_id = {station_id} AND arrival_time >= '{start_date}'
        """).pl()

    chart = plot_accumulated_arrivals(arrivals_df)

    # Placeholder for stats calculation
    statistics = {
        "station": station_id
    }


    return render_template("stats.html", train=train, station=station, statistics=statistics)

if __name__ == '__main__':
    app.run(debug=True)
