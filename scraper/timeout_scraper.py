import requests
from bs4 import BeautifulSoup
from .sources import HAPPY_HOUR_SOURCES

# Pull our URL list from the central sources config
from scraper.sources import HAPPY_HOUR_SOURCES

def scrape_happy_hours():
    # Loop through every source URL we've defined
    for url in HAPPY_HOUR_SOURCES:
        print(f"\nScraping: {url}")

        # Send the HTTP GET — like your browser visiting the page
        response = requests.get(url)

        # Parse the raw HTML into something navigable
        soup = BeautifulSoup(response.text, "html.parser")

        # Print the page title to confirm we connected
        print(f"Page title: {soup.title.text}")

if __name__ == "__main__":
    scrape_happy_hours()