from client import DigitrafficClient
import duckdb
import polars as pl

with duckdb.connect("uusikaupunki.duckdb") as con:

    client = DigitrafficClient()
    stations = client.get_stations()

    df = pl.DataFrame(stations)

    df = df.filter(pl.col("countryCode") == "FI")

    df = df.select([
        pl.col("stationUICCode").alias("id"),
        pl.col("stationName").alias("name")
    ])

    con.execute("""
        DROP TABLE IF EXISTS stations;
        """)

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
        CREATE OR REPLACE SEQUENCE train_arrival_id_seq START 1;
        """)

    con.execute("""
        DROP TABLE IF EXISTS train_arrivals;
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
