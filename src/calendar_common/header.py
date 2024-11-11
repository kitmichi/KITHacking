from datetime import datetime, timedelta

from icalendar import Calendar, Timezone, TimezoneDaylight, TimezoneStandard


def add_timezone(calendar):
    timezone = Timezone()
    timezone.add("TZID", "Europe/Berlin")
    timezone.add("X-LIC-LOCATION", "Europe/Berlin")

    daylight = TimezoneDaylight()
    daylight.add("TZOFFSETFROM", timedelta(hours=1))
    daylight.add("TZOFFSETTO", timedelta(hours=2))
    daylight.add("TZNAME", "CEST")
    daylight.add("DTSTART", datetime(1970, 3, 29, 2, 0, 0))
    daylight.add(
        "RRULE", {"FREQ": "YEARLY", "INTERVAL": 1, "BYDAY": "-1SU", "BYMONTH": 3}
    )
    timezone.add_component(daylight)

    standard = TimezoneStandard()
    standard.add("TZOFFSETFROM", timedelta(hours=2))
    standard.add("TZOFFSETTO", timedelta(hours=1))
    standard.add("TZNAME", "CET")
    standard.add("DTSTART", datetime(1970, 10, 25, 3, 0, 0))
    standard.add(
        "RRULE", {"FREQ": "YEARLY", "INTERVAL": 1, "BYDAY": "-1SU", "BYMONTH": 10}
    )
    timezone.add_component(standard)

    calendar.add_component(timezone)


def create_calendar_with_header():
    calendar = Calendar()
    calendar.add("version", "2.0")
    add_timezone(calendar)
    return calendar
