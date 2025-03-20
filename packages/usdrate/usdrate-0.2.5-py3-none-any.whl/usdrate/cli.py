#!/usr/bin/env python3
import argparse
import re
import os
import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import arrow
import base64
import time

from logflex.logflex import CustomLogger
logger = CustomLogger('usdrate', loglevel='INFO', verbose=False, trace=False, color_enable=True)

# Selenium imports (used for PDF output)
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ImportError:
    webdriver = None
    Options = None

def get_cache_dir():
    """Return the path to the 'cache' folder located in the same directory as this script."""
    return os.path.join(os.path.dirname(__file__), 'cache')

def extract_data_from_html(html):
    """
    Extract the year (in the format (XXXX年)) from the title of the Shift_JIS encoded HTML,
    and return a DataFrame containing the mid rate data for each day from the table.
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

    for row in rows[1:]:
        cells = row.find_all(['th', 'td'])
        if not cells:
            continue

        day_text = cells[0].get_text(strip=True)
        if not re.fullmatch(r'\d{1,2}', day_text):
            continue  # Skip rows such as "Monthly Average"

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
            date_str = f"{year}-{month:02d}-{day:02d}"
            data.append({'date': date_str, 'mid_rate': rate})
    return pd.DataFrame(data)

def fetch_data_for_year(year, retries=3, delay=3):
    """Fetch the HTML for the specified year and return it as a DataFrame, with retry logic."""
    url = f"https://www.77bank.co.jp/kawase/usd{year}.html"
    logger.info(f"Fetching data for year {year} from {url} ...")
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url)
            response.encoding = 'shift_jis'
            html = response.text
            df_year = extract_data_from_html(html)
            return df_year
        except Exception as e:
            logger.error(f"Attempt {attempt} failed to fetch data for year {year}: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise

def save_as_pdf(url, output_path, retries=3, delay=3):
    """
    Use Selenium's headless Chrome to convert the specified URL page to a PDF
    and save it to output_path. Retries if an error occurs.
    """
    if webdriver is None or Options is None:
        raise RuntimeError("Selenium is not imported. PDF output is not available.")
    for attempt in range(1, retries + 1):
        driver = None
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            # Use DevTools protocol to generate the PDF
            pdf = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
            pdf_data = base64.b64decode(pdf['data'])
            with open(output_path, 'wb') as f:
                f.write(pdf_data)
            driver.quit()
            logger.info(f"PDF saved to: {output_path}")
            return
        except Exception as e:
            logger.error(f"Attempt {attempt} failed to create PDF: {e}")
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass
            if attempt < retries:
                time.sleep(delay)
            else:
                raise

def ensure_pdf_files(pdf_dir):
    """
    Check if the PDF for each target year (e.g., usd2024.pdf) exists in the cache/pdfs folder;
    if the year is the current year or the PDF is missing, download it with retry logic.
    """
    current_year = datetime.datetime.now().year
    start_year = current_year - 7
    for year in range(start_year, current_year + 1):
        url = f"https://www.77bank.co.jp/kawase/usd{year}.html"
        base_filename = os.path.basename(url)  # e.g., "usd2024.html"
        pdf_filename = os.path.splitext(base_filename)[0] + ".pdf"  # e.g., "usd2024.pdf"
        pdf_file_path = os.path.join(pdf_dir, pdf_filename)
        # For current year, always update; for past years, update only if missing.
        if year == current_year or not os.path.exists(pdf_file_path):
            try:
                save_as_pdf(url, pdf_file_path)
            except Exception as e:
                print(f"Failed to create PDF: {e}")
                print("ChromeDriver may not be installed.")
                print("Please download and configure ChromeDriver from:")
                print("https://googlechromelabs.github.io/chrome-for-testing/")

def update_cache(cache_path, pdf_output=False, pdf_dir=None):
    """
    Fetch data for the current year and the past 7 years, concatenate the data,
    and cache it as a CSV. If pdf_output is True, also generate PDFs for each year.
    For the current year, the PDF is always updated.
    """
    current_year = datetime.datetime.now().year
    start_year = current_year - 7
    all_dfs = []

    for year in range(start_year, current_year + 1):
        url = f"https://www.77bank.co.jp/kawase/usd{year}.html"
        try:
            df_year = fetch_data_for_year(year)
            all_dfs.append(df_year)
            if pdf_output and pdf_dir:
                base_filename = os.path.basename(url)
                pdf_filename = os.path.splitext(base_filename)[0] + ".pdf"
                pdf_file_path = os.path.join(pdf_dir, pdf_filename)
                # Always update PDF for current year, else update only if missing.
                if year == current_year or not os.path.exists(pdf_file_path):
                    try:
                        save_as_pdf(url, pdf_file_path)
                    except Exception as e:
                        print(f"Failed to create PDF: {e}")
                        print("ChromeDriver may not be installed.")
                        print("Please download and configure ChromeDriver from:")
                        print("https://googlechromelabs.github.io/chrome-for-testing/")
        except Exception as e:
            print(f"Failed to fetch or parse data for {year}: {e}")

    if not all_dfs:
        logger.warn("No data fetched.")
        return None

    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_df['date'] = pd.to_datetime(combined_df['date'])
    combined_df = combined_df.sort_values('date')

    combined_df.to_csv(cache_path, index=False)
    logger.info(f"Data saved to cache: {cache_path}")
    return combined_df

def query_rate(query_date_str, df):
    """Display the mid rate for the date specified by the argument."""
    try:
        query_date = arrow.get(query_date_str).date()
    except Exception as e:
        logger.error(f"Failed to parse the date: {e}")
        return

    df['date'] = pd.to_datetime(df['date']).dt.date
    result = df[df['date'] == query_date]
    if not result.empty:
        mid_rate = result.iloc[0]['mid_rate']
        print(f"The USD/JPY mid rate on {query_date} is {mid_rate}.")
    else:
        print(f"No data found for {query_date}.")

def main():
    is_updated = False
    parser = argparse.ArgumentParser(
        description="Fetch and cache USD/JPY mid rate data from the 77bank exchange rate website "
                    "for the current year and the past 7 years, and query the mid rate for a specified date."
    )
    parser.add_argument("date", nargs="?", help="The date to query (e.g., 2024/3/1, March 1, 2024, etc.)")
    parser.add_argument('-b', '--bulk', help="File containing newline-separated dates to query.")
    parser.add_argument('--update', '-u', action='store_true', help="Force update the cache")
    parser.add_argument('-p', '--pdfoutput', action='store_true', help="Download and save PDF along with HTML retrieval")
    args = parser.parse_args()

    cache_dir = get_cache_dir()
    cache_file = "cache.csv"
    cache_path = os.path.join(cache_dir, cache_file)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        logger.info(f"Created cache directory: {cache_dir}")

    pdf_dir = None
    if args.pdfoutput:
        pdf_dir = os.path.join(cache_dir, "pdfs")
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
            logger.info(f"Created PDF directory: {pdf_dir}")

    # If no date and no bulk file are provided, allow running in PDF-only mode
    if not args.date and not args.bulk:
        if args.pdfoutput:
            ensure_pdf_files(pdf_dir)
            logger.info("PDF download completed.")
            return
        else:
            print("No date provided. Please specify a date or provide a bulk file using -b.")
            return

    # Update the cache if it doesn't exist, is empty, or the -u option is specified
    if not os.path.exists(cache_path) or os.path.getsize(cache_path) == 0 or args.update:
        df = update_cache(cache_path, pdf_output=args.pdfoutput, pdf_dir=pdf_dir)
        if df is None:
            return
        else:
            is_updated = True
    else:
        try:
            df = pd.read_csv(cache_path)
        except Exception as e:
            print(f"Failed to read the cache CSV file: {e}")
            return

    # When the -p option is specified, check for PDF file existence and update current year if needed
    if args.pdfoutput and pdf_dir and not is_updated:
        ensure_pdf_files(pdf_dir)

    # Process bulk file if provided, otherwise process the single date argument
    if args.bulk:
        try:
            with open(args.bulk, 'r') as f:
                for line in f:
                    date_str = line.strip()
                    if date_str:
                        query_rate(date_str, df)
        except Exception as e:
            logger.error(f"Failed to read bulk file: {e}")
    else:
        query_rate(args.date, df)

if __name__ == "__main__":
    main()
