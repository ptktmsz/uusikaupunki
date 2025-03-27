# Uusikaupunki webapp

This is a Flask web application that retrieves and analyzes train timetable data from the Finnish railway system. It stores data in a **DuckDB** database and provides a web interface for querying train arrivals at different stations.

## Features
- Ingest train timetable data from the Digitraffic API into DuckDB database.
- Web interface to select trains and stations displaying the average train arrival times over a period of 30 days.

## Installation
### Prerequisites
- **Python 3.10+**
- **DuckDB** installed (`pip install duckdb`)
- **Polars** for efficient DataFrame operations (`pip install polars`)
- **Flask** for the web interface (`pip install flask`)

## Setup
1. Clone the repository.
   ```sh
   git clone git clone https://github.com/ptktmsz/uusikaupunki.git
   ```
2. Create a virtual environment and activate it.
3. Install dependencies from requirements.txt or via uv .toml.

## Usage
### 1. Create the database:
```sh
python db/init_db.py
```
### 2. Ingest the timetable data:
Specify the train ID and date from which you want to ingest data:
```sh
python ingest.py <train_id> --date YYYY-MM-DD --backfill
```

### 3. Start the app:
```sh
python app.py
```
Visit `http://127.0.0.1:5000/` in your browser.

## API endpoints

TBD

## Database structure

TBD

## Running tests

To perform the unit tests, run:
```sh
pytest unit_tests/
```

## Future improvements
- Plotting charts with the data instead of just calculating mean (cumulated bar chart ideally).
- Feature to select the time period.
- Automated ingestion process.
- Dynamic population of `station` field based on the `train` selected.
- Nicer UI.
- Containerize the app using Docker.
- Expand the database.

## License
MIT License. Feel free to use and modify!