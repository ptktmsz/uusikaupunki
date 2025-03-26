from etl.client import DigitrafficClient
import duckdb
import os
import polars as pl

db_path = "db/uusikaupunki.duckdb"

if os.path.exists(db_path):
    os.remove(db_path)

with duckdb.connect(db_path) as con:
    client = DigitrafficClient()
    stations = client.get_stations()

    df = pl.DataFrame(stations)

    df = df.filter(pl.col("countryCode") == "FI")

    df = df.select([
        pl.col("stationUICCode").alias("id"),
        pl.col("stationName").alias("name")
    ])

    con.execute("""
        CREATE TABLE stations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
        )
        """)

    con.execute("""
        INSERT INTO stations SELECT * FROM df
        """)

    con.execute("""
        CREATE SEQUENCE train_arrival_id_seq START 1;
        """)

    con.execute("""
        CREATE TABLE train_arrivals (
            id BIGINT PRIMARY KEY,
            train_id INTEGER,
            station_id INTEGER,
            departure_time TIMESTAMP,
            arrival_time TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (station_id) REFERENCES stations (id)
        )
    """)
