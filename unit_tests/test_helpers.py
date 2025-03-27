from datetime import datetime, time

import polars as pl

from helpers import get_average_time


def test_get_average_time():
    df = pl.DataFrame({
        "arrival_time": [
            datetime(2024, 3, 23, 10, 30, 0),
            datetime(2024, 3, 24, 11, 0, 0),
            datetime(2024, 3, 25, 11, 30, 0),
        ]
    })

    avg_time = get_average_time(df=df, timecol="arrival_time")

    assert avg_time == time(11, 0, 0), f"Expected 11:00:00 but got {avg_time}"


def test_get_average_time_empty_df():
    # Empty DataFrame case
    df = pl.DataFrame({"arrival_time": []})

    avg_time = get_average_time(df=df, timecol="arrival_time")

    assert avg_time is None, f"Expected None for empty DataFrame but got {avg_time}"
