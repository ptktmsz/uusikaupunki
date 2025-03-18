import pandas as pd
import requests

def main():
    date = "2025-03-17"
    train = "27"
    url = f"https://rata.digitraffic.fi/api/v1/trains/{date}/{train}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        print(df)
    else:
        print(f"Error: {response.status_code}")


if __name__ == "__main__":
    main()
