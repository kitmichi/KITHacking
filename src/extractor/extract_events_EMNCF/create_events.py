import logging
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from icalendar import Calendar, Event, Timezone, TimezoneDaylight, TimezoneStandard
from tabulate import tabulate


# Function to get the weekday of a date
def get_weekday(date_str):
    date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    return date_obj.strftime("%A")


def extract_table_data(base_dir: Path):
    table = pd.DataFrame(columns=["Weekday", "Date", "Time", "Event"])
    row_counter = 0
    for event in ["Lecture", "Exercise"]:
        path_to_list = base_dir / f"{event}.txt"
        if not path_to_list.exists():
            continue
        path_to_events_negative = base_dir / f"{event} negative.txt"
        events_negative = []
        if path_to_events_negative.exists():
            events_negative = [
                line.strip()
                for line in path_to_events_negative.read_text().strip().splitlines()
            ]
        with open(path_to_list, "r") as f:
            for i, line in enumerate(
                [line for line in f.readlines() if line.strip() not in events_negative]
            ):
                date = line.strip()
                event2 = f"{event} {i + 1}"
                weekday = get_weekday(date)
                if weekday == "Tuesday":
                    time = "17:30 – 19:00"
                if weekday == "Thursday":
                    time = "17:30 – 19:00"
                table.loc[row_counter] = [weekday, date, time, event2]
                row_counter += 1

    # Convert the 'Date' column to datetime format
    table["datetime"] = pd.to_datetime(table["Date"], format="%d.%m.%Y")

    # Sort the table by the 'Date' column
    table = table.sort_values(by="datetime")

    table = table.reset_index(drop=True)
    table = table.drop(columns=["datetime"])

    return table


def parse_datetime(date_str, time_str):
    start_time, end_time = time_str.split("–")
    start_datetime = datetime.strptime(date_str + start_time.strip(), "%d.%m.%Y%H:%M")
    end_datetime = datetime.strptime(date_str + end_time.strip(), "%d.%m.%Y%H:%M")
    return start_datetime, end_datetime


def create_event(row):
    event = Event()
    details = row["Event"]
    start_datetime, end_datetime = parse_datetime(row["Date"], row["Time"])
    event.add("dtstart", start_datetime, parameters={"TZID": "Europe/Berlin"})
    event.add("dtend", end_datetime, parameters={"TZID": "Europe/Berlin"})
    event.add("dtstamp", datetime.now())
    if row["Weekday"] == "Tuesday":
        location = "30.34 Lichttechnik-Hörsaal (LTI)"
    if row["Weekday"] == "Thursday":
        location = "10.91 Mittlerer Hörsaal Maschinenbau"
    event.add("location", location)

    if "Exercise" in details:
        summary = (
            "2308265 - Exercise for "
            "2308263 Electromagnetics and Numerical Calculation of Fields (Ü), "
            "Pauli et al., ETIT"
        )
        url = "https://campus.studium.kit.edu/ev/66gVzbxFRY2Mr0zSgj2hmA"
    else:
        summary = (
            "2308263 - Electromagnetics and Numerical Calculation of Fields (V), "
            "Pauli, ETIT"
        )
        url = "https://campus.studium.kit.edu/ev/wHv_RhD7RGWklEIWq8gZ4g"
    event.add("summary", summary)
    event.add("description", "\n".join([details, url]))
    event.add("url", url)

    return event


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


def write_files(base_dir: Path):
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    table = extract_table_data(base_dir)
    tsv = base_dir / "events.tsv"
    table.to_csv(tsv, sep="\t", index=False)

    calendar = Calendar()
    add_timezone(calendar)
    for irow in range(table.shape[0]):
        event = create_event(table.iloc[irow])
        calendar.add_component(event)

    ics = base_dir / "events.ics"
    with open(ics, "wb") as f:
        f.write(calendar.to_ical())
    logging.info("ICS file updated successfully.")
    markdown_table = tabulate(table, headers="keys", tablefmt="pipe")
    print(markdown_table)
    md = base_dir / "events.md"
    with open(md, "w") as f:
        f.write(markdown_table)
    return tsv, ics, md


if __name__ == "__main__":
    write_files(Path(__file__).parent)
