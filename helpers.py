import duckdb
import polars as pl
from datetime import datetime, timedelta

def db_get_trains() -> list:
    with duckdb.connect("db/uusikaupunki.duckdb") as con:
        res = con.execute("""SELECT DISTINCT train_id FROM train_arrivals ORDER BY train_id""")
        return [i[0] for i in res.fetchall()]

def db_get_stations() -> list:
    with duckdb.connect("db/uusikaupunki.duckdb") as con:
        res = con.execute(f"""SELECT DISTINCT name FROM stations ORDER BY name""")
        return [i[0] for i in res.fetchall()]

def find_station_id(station: str) -> int:
    with duckdb.connect("db/uusikaupunki.duckdb") as con:
        res = con.execute(f"""SELECT id FROM stations WHERE name = '{station}'""")
        return res.fetchone()[0]

def plot_accumulated_arrivals(df: pl.DataFrame):
    ...