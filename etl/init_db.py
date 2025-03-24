import duckdb

con = duckdb.connect("uusikaupunki.duckdb")

con.execute("""
    CREATE TABLE IF NOT EXISTS train_arrivals (
        id BIGINT PRIMARY KEY,
        train_id INTEGER,
        station_code TEXT,
        arrival_time TIMESTAMP,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

con.close()
