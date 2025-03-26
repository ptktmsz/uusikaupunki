import duckdb

def db_get_trains() -> list:
    with duckdb.connect("db/uusikaupunki.duckdb") as con:
        res = con.execute("""SELECT DISTINCT train_id FROM train_arrivals ORDER BY train_id""")
        return [i[0] for i in res.fetchall()]

def db_get_stations() -> list:
    with duckdb.connect("db/uusikaupunki.duckdb") as con:
        res = con.execute(f"""SELECT DISTINCT name FROM stations ORDER BY name""")
        return [i[0] for i in res.fetchall()]
