import duckdb
from etl.client import DigitrafficClient
import polars as pl

def ingest_timetable(date: str, train: str) -> None:
    client = DigitrafficClient()
    train_trip = client.get_train_trip(date, train)
    timetable = train_trip["timeTableRows"]
    df = pl.from_dicts(timetable)
    df = df.select(["stationUICCode", "type", "actualTime"])
    df = df.with_columns(pl.col("actualTime").str.to_datetime())
    df = df.pivot("type", index="stationUICCode", values="actualTime")
    with duckdb.connect("uusikaupunki.duckdb") as con:
        con.execute(
            f"""
            INSERT INTO train_arrivals (id, train_id, station_id, departure_time, arrival_time)
            SELECT nextval('train_arrival_id_seq'), {train}, stationUICCode, DEPARTURE, ARRIVAL FROM df
            """
        )

ingest_timetable("2025-03-23", "27")
