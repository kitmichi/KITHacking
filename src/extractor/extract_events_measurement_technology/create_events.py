import re
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import recurring_ical_events
from icalendar import (
    Calendar,
    Component,
    Event,
)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tabulate import tabulate
from webdriver_manager.chrome import ChromeDriverManager
from zoneinfo import ZoneInfo

from calendar_common.header import create_calendar_with_header
from ilias.login import Login


class DriverManager:
    def __init__(self):
        pass

    def __enter__(self):
        options = Options()

        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def get_events_from_ilias():
    events: list[str] = []
    with DriverManager() as driver:
        ilias_helper = Login()
        logged_in = ilias_helper.login(driver)
        if not logged_in:
            return events
        url = (
            "https://ilias.studium.kit.edu/ilias.php?"
            "baseClass=ilrepositorygui&ref_id=2479923"
        )
        driver.get(url)
        pattern = re.compile(r"\d{2}\.\d{2}\.\d{2} \d{2}:\d{2}: .+")

        # Find elements containing the pattern
        elements = driver.find_elements(By.XPATH, "//div[contains(text(), ':')]")

        # Extract and print the date, time, and description
        for element in elements:
            for text in element.text.splitlines():
                if pattern.match(text):
                    events.append(text)
    return events


def create_table_from_events(events: list[str]):
    table = pd.DataFrame(columns=["Datetime", "Duration", "Event"])
    for event in events:
        date_time, description = event.split(": ", 1)
        date_time_start = datetime.strptime(date_time, "%d.%m.%y %H:%M")
        date_time_start = date_time_start.replace(tzinfo=ZoneInfo("Europe/Berlin"))

        description = description.capitalize()
        row = pd.DataFrame(
            [
                {
                    "Datetime": date_time_start,
                    "Duration": timedelta(minutes=90),
                    "Event": description,
                }
            ]
        )
        table = pd.concat(
            [
                table,
                row,
            ],
            ignore_index=True,
        )
    return table


def get_ical_from_disk(base_dir: Path):
    with open(
        base_dir / "eventfavorites campus 2302117 – Measurement Technology.ics",
        "rb",
    ) as f:
        calendar = Calendar.from_ical(f.read())
    return calendar


def is_timespan_in_calendar(calendar, start_time: datetime, duration: timedelta):
    end_time = start_time + duration
    events = recurring_ical_events.of(calendar).between(start_time, duration)
    ret_val: list[Component] = []
    for event in events:
        event_start = event.get("dtstart").dt
        event_end = event.get("dtend").dt
        if start_time == event_start and end_time == event_end:
            ret_val.append(event)
    return ret_val


def create_event(row, old_event: Component):
    event = Event()
    details = row["Event"]
    start_datetime = row["Datetime"]
    end_datetime = start_datetime + row["Duration"]
    event.add("dtstart", start_datetime)
    event.add("dtend", end_datetime)
    event.add("dtstamp", datetime.now())
    event.add("location", old_event.get("location"))

    if "Exercise" in details:
        summary = (
            "2302118 - Exercise for "
            "2302117 Measurement Technology (Ü), Heizmann et al., ETIT"
        )
        url = "https://campus.studium.kit.edu/ev/LAnH51SMSaWn2jX-ZrojyQ"
    else:
        summary = ":2302117 - Measurement Technology (V), Heizmann, ETIT"
        url = "https://campus.studium.kit.edu/ev/lxru9u4XTliY9G6QtHP2dw"
    event.add("summary", summary)
    event.add("description", "\n".join([details, url]))
    event.add("url", url)

    return event


def fill_new_calendar(
    old_calendar: Calendar, new_calendar: Calendar, table: pd.DataFrame
):
    # Iterate through the DataFrame and check each event
    for index, row in table.iterrows():
        start_time = row["Datetime"]
        duration = row["Duration"]
        events_in_calendar = is_timespan_in_calendar(old_calendar, start_time, duration)
        if len(events_in_calendar) == 1:
            event = create_event(row, events_in_calendar[0])
            new_calendar.add_component(event)
        else:
            print(f"Event '{row['Event']}' is not in the calendar.")


def create_files(base_dir: Path, table: pd.DataFrame, new_calendar: Calendar):
    tsv = base_dir / "events.tsv"
    table.to_csv(tsv, sep="\t", index=False)
    ics = base_dir / "events.ics"
    with open(ics, "wb") as f:
        f.write(new_calendar.to_ical())
    markdown_table = tabulate(table, headers="keys", tablefmt="pipe")
    md = base_dir / "events.md"
    with open(md, "w") as f:
        f.write(markdown_table)
    return tsv, ics, md


def create_events(base_dir: Path):
    events = get_events_from_ilias()
    table = create_table_from_events(events)
    calendar = get_ical_from_disk(Path(__file__).parent)
    new_calendar = create_calendar_with_header()
    fill_new_calendar(calendar, new_calendar, table)
    return create_files(base_dir, table, new_calendar)
