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

    # Extract data from the webpage using BeautifulSoup
    # Modify this part according to the structure of the web page you're scraping

    # Example: Extracting property details like title and price
    property_listings = soup.find_all('div', class_='sc-15l4r6f-0')

    for listing in property_listings:
        # print(listing)
        title = listing.find('h2', class_='sc-1barvlq-1').text.strip()
        price = listing.find('div', class_='sc-cmkc2d-7 sc-11jo8dj-4 iZrQA-D kuRbQC').text.strip()
        location = listing.find('span', class_='MuiTypography-root').text.strip()
        sqft = listing.find('div', {'data-testid': 'listing-size'}).text.strip()
        link_div = listing.find('a', class_='sc-15l4r6f-1')
        link = link_div['href']




        # Insert data into the SQLite database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO properties (title, price, location,sqft,link) VALUES (?, ?, ?, ?,?)", (title, price, location, sqft, link))
        conn.commit()

# Create SQLite database and table
conn = sqlite3.connect('property_data.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS properties (title TEXT, price TEXT, location TEXT, sqft TEXT, link TEXT)")

# Scrape all pages
base_url = "https://dubai.dubizzle.com/property-for-rent/residential/apartmentflat/?bedrooms=1&page="
total_pages = 412  # Modify this value based on the total number of pages to scrape

for page in range(1, total_pages + 1):
    url = base_url + str(page)
    scrape_page(url, conn)

# Close the database connection
conn.close()
