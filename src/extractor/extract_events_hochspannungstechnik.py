import logging
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from icalendar import Calendar, Event, Timezone, TimezoneDaylight, TimezoneStandard
from tabulate import tabulate

from extractor.pdf_table_extractor import extract_table
from ilias.pdf_downloader import PdfDownloader


def extract_table_data(pdf_path):
    try:
        table = extract_table(pdf_path)
        logging.info("Table extracted successfully.")
        return table
    except FileNotFoundError:
        logging.error("PDF file not found.")
        exit(1)


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
    event.add("location", "30.35 Hochspannungstechnik-Hörsaal (HSI)")

    if "Übung" in details:
        summary = (
            "2307362 - Übungen zu 2307360 Hochspannungstechnik  (Ü), "
            "Badent et al., ETIT"
        )
        url = "https://campus.studium.kit.edu/ev/uUhpKvm2TZCgiRBTWSKnUQ"
    else:
        summary = "2307360 - Hochspannungstechnik  (V), Badent, ETIT"
        url = "https://campus.studium.kit.edu/ev/vcoe0X2xQFKvAGeWS_QKwg"
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


def write_files(base_dir: Path, pdf_url: str):
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp_dir:
        pdf_downloader = PdfDownloader(
            Path(temp_dir),
            pdf_url,
        )
        pdf_path = pdf_downloader.download()
        table = extract_table_data(pdf_path)
    table.columns = ["Weekday", "Date", "Time", "Event"]
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
    write_files(
        Path(__file__).parent,
        (
            "https://ilias.studium.kit.edu/login.php?"
            "client_id=produktiv&cmd=force_login&lang=de"
        ),
    )
