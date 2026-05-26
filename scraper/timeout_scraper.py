import os
import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from venues.models import Venue, HappyHour

NEIGHBORHOOD_URLS = [
    ('River North', 'https://www.312deals.com/happy-hours/river-north'),
]

def parse_card(card, neighborhood):
    parts = card.get_text(separator='|', strip=True).split('|')
    slug = card['href'].replace('/venues/', '')
    name = slug.replace('-', ' ').title()
    deal = parts[4] if len(parts) > 4 else None
    days = None
    times = None
    for part in parts:
        if 'AM' in part or 'PM' in part:
            times = part
        elif any(d in part for d in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Every']):
            days = part
    return name, neighborhood, days, times, deal

def scrape():
    for neighborhood, url in NEIGHBORHOOD_URLS:
        print(f"\nScraping {neighborhood}...")
        r = requests.get(url)
        if r.status_code != 200:
            print(f"  Skipping — status {r.status_code}")
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
        cards = soup.find_all('a', href=lambda h: h and h.startswith('/venues/'))
        print(f"  Found {len(cards)} cards")
        for card in cards:
            name, neighborhood, days, times, deal = parse_card(card, neighborhood)
            if not name or not times:
                continue
            venue, _ = Venue.objects.get_or_create(
                name=name,
                neighborhood=neighborhood,
                defaults={'address': ''}
            )
            HappyHour.objects.filter(venue=venue).delete()
            HappyHour.objects.create(
                venue=venue,
                day_of_week=days or '',
                start_time='00:00',
                end_time='00:00',
                deal=deal or '',
                source='312deals',
                last_verified=None
            )
            print(f"  Saved: {name}")

if __name__ == '__main__':
    scrape()