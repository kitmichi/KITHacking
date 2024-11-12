from datetime import datetime
from pathlib import Path

import recurring_ical_events
from icalendar import Calendar, Component
from zoneinfo import ZoneInfo

from calendar_common.header import create_calendar_with_header


def get_ical_from_disk(base_dir: Path):
    with open(
        base_dir / "eventfavorites campus 2307392 – Hochspannungsprüftechnik.ics",
        "rb",
    ) as f:
        calendar = Calendar.from_ical(f.read())
    return calendar


def get_all_lectures(calendar):
    start_date = datetime.strptime("24.10.2024", "%d.%m.%Y").replace(
        tzinfo=ZoneInfo("Europe/Berlin")
    )
    events = recurring_ical_events.of(calendar).after(start_date)
    ret_val: list[Component] = []
    for event in events:
        if (
            event.get("summary")
            == "2307392 - Hochspannungsprüftechnik (V), Badent, ETIT"
        ):
            ret_val.append(event)
    return ret_val


def create_ics(events: list[Component], base_dir: Path):
    calendar = create_calendar_with_header()
    for event in events:
        calendar.add_component(event)
    ics = base_dir / "events.ics"
    with open(ics, "wb") as f:
        f.write(calendar.to_ical())
    return ics


def create_events(base_dir: Path):
    calendar = get_ical_from_disk(Path(__file__).parent)
    all_lectures = get_all_lectures(calendar)
    ics = create_ics(all_lectures, base_dir)
    return ics
