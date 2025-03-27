import duckdb
import polars as pl
from datetime import datetime

DB_PATH = "db/uusikaupunki.duckdb"

def db_get_trains() -> list:
    """Returns list of distinct train IDs in the database of train arrivals."""
    with duckdb.connect("db/uusikaupunki.duckdb") as con:
        res = con.execute("SELECT DISTINCT train_id FROM train_arrivals ORDER BY train_id")
        return [i[0] for i in res.fetchall()]

def db_get_stations() -> list:
    """Returns list of distinct station names in the database of train arrivals."""
    with duckdb.connect("db/uusikaupunki.duckdb") as con:
        res = con.execute("SELECT DISTINCT name FROM stations ORDER BY name")
        return [i[0] for i in res.fetchall()]

def find_station_id(station: str) -> int | None:
    """
    Converts the station name to station ID.
    :param station: station name as astring
    :return: station ID as an integer.
    """
    with duckdb.connect("db/uusikaupunki.duckdb") as con:
        res = con.execute("SELECT id FROM stations WHERE name = ?", [station]).fetchone()
        return res[0] if res else None

def get_average_time(df: pl.DataFrame, timecol: str) -> datetime.time:
    """
    Gets the average time from a given dataframe disregarding the date.
    :param df: polars dataframe to be processed.
    :param timecol: name of the timestamp column with datetime data.
    :return: average time object as a datetime.time.
    """
    times = df[timecol].dt.time()
    # Time objects cannot be calculated easily, so adding current date to create a datetime object.
    datetimes = pl.Series(datetime.combine(datetime.today().date(), t) for t in times)
    # Converting back to time to get rid of the date and returning.
    return datetimes.mean().time()
