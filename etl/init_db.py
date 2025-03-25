import duckdb

with duckdb.connect("uusikaupunki.duckdb") as con:
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
            FOREIGN KEY (station_id) REFERENCES stations (station_id)
        )
    """)

    con.execute("""
        CREATE TABLE stations (
        id BIGINT PRIMARY KEY,
        name TEXT NOT NULL,
        )
    """)