import os

import duckdb
import polars as pl

from etl.client import DigitrafficClient

DB_PATH = "db/uusikaupunki.duckdb"

def reset_database(path: str) -> None:
    """
    If database exists, it removes it.
    :param path: path to the database from root.
    :return: None.
    """
    if os.path.exists(path):
        os.remove(path)
        print("Database removed.")


def create_and_populate_stations_table(con: duckdb.DuckDBPyConnection) -> None:
    """
    :param con: duckDB connection to the database.
    :return: None.
    """
    client = DigitrafficClient()
    stations = client.get_stations()
    df = pl.DataFrame(stations)
    df = df.filter(pl.col("countryCode") == "FI") # keeping only Finnish stations to avoid duplicate IDs
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


def create_train_arrivals_table(con: duckdb.DuckDBPyConnection) -> None:
    """
    :param con: duckDB connection to the database.
    :return: None.
    """
    con.execute("""CREATE SEQUENCE train_arrival_id_seq START 1""")

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


if __name__ == "__main__":
    reset_database(DB_PATH)
    with duckdb.connect(DB_PATH) as connnection:
        create_and_populate_stations_table(connnection)
        create_train_arrivals_table(connnection)
        print("Database recreated.")
