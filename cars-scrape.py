import requests
import time
from bs4 import BeautifulSoup
import sqlite3

# Function to scrape a single page and insert data into the database
def scrape_page(url, conn):


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    print("url " + url)
    soup = BeautifulSoup(response.text, 'html.parser')


    time.sleep(1)


    property_listings = soup.find_all('div', class_='sc-cmkc2d-0 iJUziq dbz-ads-listing')


    for listing in property_listings:
        link_div = listing.find('a', class_='sc-cmkc2d-1 sc-cmkc2d-2 jGrTEY fGnHWp')
        link = link_div['href']


        # print(listing)
        title = listing.find('div', class_='sc-12jmuzh-0 jZA-dVl heading').text.strip()
        location = listing.find('div', class_='sc-cmkc2d-24 hOpXgZ').text.strip()
        price = listing.find('div', class_='sc-11jo8dj-0 fNUWAC').text.strip()
        year = listing.find('div', class_='sc-cmkc2d-11 cwhBN summary-wrapper').text.strip()






        # Insert data into the SQLite database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cars (title, price, location,link, year) VALUES (?, ?, ?, ?,?)", (title, price, location, link, year))
        conn.commit()

# Create SQLite database and table
conn = sqlite3.connect('property_data.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS cars (title TEXT, price TEXT, location TEXT, link TEXT, year TEXT)")

# Scrape all pages
base_url = "https://dubai.dubizzle.com/motors/used-cars/?kilometers__gte=0&kilometers__lte=150000&year__gte=2012&year__lte=2019&page="
total_pages = 392  # Modify this value based on the total number of pages to scrape

for page in range(1, total_pages + 1):
    url = base_url + str(page)
    scrape_page(url, conn)

# Close the database connection
conn.close()
