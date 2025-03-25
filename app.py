from flask import Flask, redirect, render_template, request, url_for
from helpers import get_stations, get_trains

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def select_train():
    if request.method == "POST":
        selected_train = request.form.get("train")
        if selected_train:
            return redirect(url_for("select_station", train_id=selected_train))

    trains = get_trains()
    return render_template("select_train.html", trains=trains)


@app.route("/select_station/<train_id>", methods=["GET", "POST"])
def select_station(train_id):
    stations = get_stations(train_id)
    if request.method == "POST":
        selected_station = request.form.get("station")
        if selected_station:
            return redirect(url_for("show_results", train_id=train_id, station_id=selected_station))

    return render_template("select_station.html", train_id=train_id, stations=stations)


@app.route("/results/<train_id>/<station_id>")
def show_results(train_id, station_id):
    return f"Showing results for Train {train_id} at Station {station_id}"


if __name__ == '__main__':
    app.run(debug=True)
