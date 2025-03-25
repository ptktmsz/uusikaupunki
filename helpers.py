import duckdb

def get_trains() -> list:
    with duckdb.connect("etl/uusikaupunki.duckdb") as con:
        res = con.execute("""SELECT DISTINCT train_id FROM train_arrivals ORDER BY train_id""")
        return [i[0] for i in res.fetchall()]

def get_stations(train: int) -> list:
    with duckdb.connect("etl/uusikaupunki.duckdb") as con:
        res = con.execute(f"""SELECT DISTINCT station_id FROM train_arrivals WHERE train_id = {train} ORDER BY train_id""")
        return [i[0] for i in res.fetchall()]
