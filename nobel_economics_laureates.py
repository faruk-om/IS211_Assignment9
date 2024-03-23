# nobel_economics_laureates.py
# Script to scrape the list of Nobel Memorial Prize laureates in Economics from Wikipedia
# Wikipedia URL: https://en.wikipedia.org/wiki/List_of_Nobel_Memorial_Prize_laureates_in_Economic_Sciences

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_nobel_economics_laureates(url):
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to retrieve the webpage')
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = table.find_all('tr')
    table_data = []
    for row in rows:
        columns = row.find_all('td')
        if columns:
            columns = [column.text.strip() for column in columns]
            table_data.append(columns)

    df = pd.DataFrame(table_data, columns=headers)
    df = df.replace(r'\[\d+\]', '', regex=True)  # Remove citation references
    return df

if __name__ == "__main__":
    URL = 'https://en.wikipedia.org/wiki/List_of_Nobel_Memorial_Prize_laureates_in_Economic_Sciences'
    df_laureates = scrape_nobel_economics_laureates(URL)
    if df_laureates is not None:
        print(df_laureates.head())
        df_laureates.to_csv('nobel_economics_laureates.csv', index=False)
