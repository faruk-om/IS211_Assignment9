# nba_champions.py
# Script to scrape the list of NBA champions from Wikipedia
# Wikipedia URL: https://en.wikipedia.org/wiki/List_of_NBA_champions

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_nba_champions(url):
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to retrieve the webpage')
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table', {'class': 'wikitable'})[-1]  # The champions table is usually the last one
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
    URL = 'https://en.wikipedia.org/wiki/List_of_NBA_champions'
    df_champions = scrape_nba_champions(URL)
    if df_champions is not None:
        print(df_champions.head())
        df_champions.to_csv('nba_champions.csv', index=False)
