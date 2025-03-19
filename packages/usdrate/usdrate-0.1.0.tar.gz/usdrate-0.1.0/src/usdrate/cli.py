#!/usr/bin/env python3
import argparse
import re
import os
import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import arrow

def get_cache_dir():
    """
    Returns the cache directory located within the package (i.e., a 'cache' folder 
    in the same directory as this script).
    """
    return os.path.join(os.path.dirname(__file__), 'cache')

def extract_data_from_html(html):
    """
    Extracts the year from the title of the given HTML (Shift_JIS encoded) using the 
    format "(XXXX年)" and returns a DataFrame containing the mid rates for each day 
    extracted from the table.
    """
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string
    year_match = re.search(r'（(\d{4})年）', title)
    if not year_match:
        raise ValueError("Failed to extract the year from the page title.")
    year = year_match.group(1)

    table = soup.find('table')
    if table is None:
        raise ValueError("No table found in the HTML.")

    rows = table.find_all('tr')
    data = []

    # Process rows after the header row
    for row in rows[1:]:
        cells = row.find_all(['th', 'td'])
        if not cells:
            continue

        day_text = cells[0].get_text(strip=True)
        if not re.fullmatch(r'\d{1,2}', day_text):
            continue  # Skip entries such as "Monthly Average"

        day = int(day_text)
        # Columns 2 to 13 correspond to January through December
        for month, cell in enumerate(cells[1:13], start=1):
            rate_text = cell.get_text(strip=True)
            if not rate_text or rate_text in ('', '\xa0'):
                continue
            try:
                rate = float(rate_text)
            except ValueError:
                continue
            # Construct the date string (YYYY-MM-DD)
            date_str = f"{year}-{month:02d}-{day:02d}"
            data.append({'date': date_str, 'mid_rate': rate})

    return pd.DataFrame(data)

def fetch_data_for_year(year):
    """
    Fetches the HTML for the specified year from the URL, extracts the data, and returns 
    it as a DataFrame.
    """
    url = f"https://www.77bank.co.jp/kawase/usd{year}.html"
    print(f"Fetching data for year {year} from {url} ...")
    response = requests.get(url)
    response.encoding = 'shift_jis'
    html = response.text
    df_year = extract_data_from_html(html)
    return df_year

def update_cache(cache_path):
    """
    Fetches data for the current year and the past 7 years (a total of 8 years), concatenates 
    the data, and saves it to the cache file.
    """
    current_year = datetime.datetime.now().year
    start_year = current_year - 7
    all_dfs = []

    for year in range(start_year, current_year + 1):
        try:
            df_year = fetch_data_for_year(year)
            all_dfs.append(df_year)
        except Exception as e:
            print(f"Failed to fetch or parse data for {year}: {e}")

    if not all_dfs:
        print("No data fetched.")
        return None

    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_df['date'] = pd.to_datetime(combined_df['date'])
    combined_df = combined_df.sort_values('date')

    # Save the combined data to the cache file
    combined_df.to_csv(cache_path, index=False)
    print(f"Data saved to cache: {cache_path}")
    return combined_df

def query_rate(query_date_str, df):
    """
    Parses the given date string using arrow and displays the mid rate for the corresponding 
    date from the cached data.
    """
    try:
        query_date = arrow.get(query_date_str).date()
    except Exception as e:
        print(f"Failed to parse the date: {e}")
        return

    df['date'] = pd.to_datetime(df['date']).dt.date
    result = df[df['date'] == query_date]
    if not result.empty:
        mid_rate = result.iloc[0]['mid_rate']
        print(f"The USD/JPY mid rate on {query_date} is {mid_rate}.")
    else:
        print(f"No data found for {query_date}.")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch and cache USD/JPY mid rate data from the 77bank exchange rate website "
                    "for the current year and the past 7 years, and query the mid rate for a specified date."
    )
    parser.add_argument("date", help="The date to query (e.g., 2024/3/1, March 1, 2024, etc.)")
    parser.add_argument('--update', '-u', action='store_true', help="Force update the cache")
    args = parser.parse_args()

    # Get the cache directory located within the package
    cache_dir = get_cache_dir()
    cache_file = "cache.csv"
    cache_path = os.path.join(cache_dir, cache_file)

    # Create the cache directory if it does not exist
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        print(f"Created cache directory: {cache_dir}")

    # If the cache file does not exist, is empty, or if the update flag is specified, fetch the data
    if not os.path.exists(cache_path) or os.path.getsize(cache_path) == 0 or args.update:
        df = update_cache(cache_path)
        if df is None:
            return
    else:
        try:
            df = pd.read_csv(cache_path)
        except Exception as e:
            print(f"Failed to read the cache CSV file: {e}")
            return

    # Query the mid rate for the date provided as the first argument
    query_rate(args.date, df)

if __name__ == "__main__":
    main()
