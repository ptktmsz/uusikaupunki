import argparse
from datetime import datetime, timedelta
import duckdb
from client import DigitrafficClient
import polars as pl

def ingest_timetable(date: str, train: str) -> None:
    client = DigitrafficClient()
    train_trip = client.get_train_trip(date, train)
    timetable = train_trip["timeTableRows"]
    df = pl.from_dicts(timetable, schema=["stationUICCode", "type", "actualTime"])
    df = df.with_columns(pl.col("actualTime").str.to_datetime())
    df = df.pivot("type", index="stationUICCode", values="actualTime")
    with duckdb.connect("db/uusikaupunki.duckdb") as con:
        con.execute(
            f"""
            INSERT INTO train_arrivals (id, train_id, station_id, departure_time, arrival_time)
            SELECT nextval('train_arrival_id_seq'), {train}, stationUICCode, DEPARTURE, ARRIVAL FROM df
            """
        )

if __name__ == '__main__':
    yesterday = datetime.today() - timedelta(days=1)
    parser = argparse.ArgumentParser()
    parser.add_argument("train", help="Train ID")
    parser.add_argument("--date", help="Date to ingest in YYYY-MM-DD  (default: yesterday)", default=yesterday.strftime("%Y-%m-%d"))
    parser.add_argument("--backfill", help="Backfill mode to ingest data from specified date until yesterday (default: False)", action="store_true")
    args = parser.parse_args()
    if args.backfill and args.date == yesterday:
        parser.error("--date is required when using --backfill")
    elif args.backfill:
        processed_date = datetime.strptime(args.date, '%Y-%m-%d')
        while processed_date < yesterday:
            ingest_timetable(processed_date.strftime("%Y-%m-%d"), args.train)
            processed_date += timedelta(days=1)
    else:
        ingest_timetable(args.date, args.train)
