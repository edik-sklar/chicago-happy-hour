import os
import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from venues.models import Venue, HappyHour

NEIGHBORHOOD_URLS = [
    ('River North', 'https://www.312deals.com/happy-hours/river-north'),
    ('Lakeview', 'https://www.312deals.com/happy-hours/lakeview'),
    ('Lincoln Park', 'https://www.312deals.com/happy-hours/lincoln-park'),
    ('The Loop', 'https://www.312deals.com/happy-hours/the-loop'),
    ('Logan Square', 'https://www.312deals.com/happy-hours/logan-square'),
    ('West Loop', 'https://www.312deals.com/happy-hours/west-loop'),
    ('West Town', 'https://www.312deals.com/happy-hours/west-town'),
    ('Portage Park', 'https://www.312deals.com/happy-hours/portage-park'),
    ('North Center', 'https://www.312deals.com/happy-hours/north-center'),
    ('Wrigleyville', 'https://www.312deals.com/happy-hours/wrigleyville'),
    ('Avondale', 'https://www.312deals.com/happy-hours/avondale'),
    ('Wicker Park', 'https://www.312deals.com/happy-hours/wicker-park'),
    ('Rogers Park', 'https://www.312deals.com/happy-hours/rogers-park'),
    ('Pilsen', 'https://www.312deals.com/happy-hours/pilsen'),
    ('Humboldt Park', 'https://www.312deals.com/happy-hours/humboldt-park'),
    ('Lincoln Square', 'https://www.312deals.com/happy-hours/lincoln-square'),
    ('Hyde Park', 'https://www.312deals.com/happy-hours/hyde-park'),
    ('Streeterville', 'https://www.312deals.com/happy-hours/streeterville'),
    ('Bucktown', 'https://www.312deals.com/happy-hours/bucktown'),
    ('South Loop', 'https://www.312deals.com/happy-hours/south-loop'),
    ('Edgewater', 'https://www.312deals.com/happy-hours/edgewater'),
    ('Bridgeport', 'https://www.312deals.com/happy-hours/bridgeport'),
    ('Andersonville', 'https://www.312deals.com/happy-hours/andersonville'),
    ('Ukrainian Village', 'https://www.312deals.com/happy-hours/ukrainian-village'),
    ('Beverly', 'https://www.312deals.com/happy-hours/beverly'),
    ('Gage Park', 'https://www.312deals.com/happy-hours/gage-park'),
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
            print(f"  days={days} times={times} deal={deal[:30] if deal else None}")
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