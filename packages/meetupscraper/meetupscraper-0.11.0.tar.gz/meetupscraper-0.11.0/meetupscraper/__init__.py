import urllib.parse
import logging
import dataclasses
import datetime
import re
from datetime import timezone
import icalendar
import requests


LOGGER = logging.getLogger("meetupscraper")
# logging.basicConfig(level='DEBUG')


@dataclasses.dataclass(frozen=True)
class Venue:
    name: str
    street: str


@dataclasses.dataclass(frozen=True)
class Event:
    url: str
    date: datetime.datetime
    title: str
    venue: Venue


def get_upcoming_events(meetup_name, name_regex=None):
    if ' ' in meetup_name:
        logging.warning('Meetup name contains spaces, replacing with hyphens')
        meetup_name = meetup_name.replace(' ', '-')
    url = f"https://meetup.com/{urllib.parse.quote(meetup_name)}/events/ical"
    LOGGER.info("Looking up %r", url)
    r = requests.get(url)

    # Parse iCal data
    cal = icalendar.Calendar.from_ical(r.content)
    logging.debug("Got iCal data")

    if name_regex:
        regex = re.compile(name_regex)
    else:
        regex = None

    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        event_name = str(component.get('summary', 'No Title'))
        event_url = str(component.get('url', ''))
        event_start = component.get('dtstart').dt
        
        if isinstance(event_start, datetime.date) and not isinstance(event_start, datetime.datetime):
            event_start = datetime.datetime.combine(event_start, datetime.time.min)
        
        if event_start.tzinfo is not None:
            event_start = event_start.astimezone(timezone.utc).replace(tzinfo=None)

        location = str(component.get('location', ''))
        venue_name = location
        venue_street = ''
        
        if ',' in location:
            venue_parts = location.split(',', 1)
            venue_name = venue_parts[0].strip()
            venue_street = venue_parts[1].strip()

        if regex and not regex.search(event_name):
            LOGGER.info("Skipping event %r", event_name)
            continue

        yield Event(
            title=event_name,
            date=event_start,
            url=event_url,
            venue=Venue(name=venue_name, street=venue_street),
        )
