import duckdb

con = duckdb.connect("uusikaupunki.duckdb")

con.execute("""
    CREATE OR REPLACE SEQUENCE train_arrival_id_seq START 1;
    """)

con.execute("""
    CREATE TABLE IF NOT EXISTS train_arrivals (
        id BIGINT PRIMARY KEY,
        train_id INTEGER,
        station_id INTEGER,
        departure_time TIMESTAMP,
        arrival_time TIMESTAMP,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

con.close()
