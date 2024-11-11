import tempfile
from pathlib import Path

from extractor.extract_events_measurement_technology.create_events import create_events


def test():
    with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp_dir:
        base_dir = Path(temp_dir)
        tsv, ics, md = create_events(base_dir)
        actual = Path(md).read_text().strip()
    expected = """
|    | Datetime                  | Duration        | Event    |
|---:|:--------------------------|:----------------|:---------|
|  0 | 2024-10-24 09:45:00+02:00 | 0 days 01:30:00 | Lecture  |
|  1 | 2024-10-31 08:00:00+01:00 | 0 days 01:30:00 | Lecture  |
|  2 | 2024-10-31 09:45:00+01:00 | 0 days 01:30:00 | Lecture  |
|  3 | 2024-11-07 08:00:00+01:00 | 0 days 01:30:00 | Exercise |
|  4 | 2024-11-14 08:00:00+01:00 | 0 days 01:30:00 | Lecture  |
|  5 | 2024-11-14 09:45:00+01:00 | 0 days 01:30:00 | Lecture  |
|  6 | 2024-11-28 08:00:00+01:00 | 0 days 01:30:00 | Exercise |
|  7 | 2024-12-05 08:00:00+01:00 | 0 days 01:30:00 | Lecture  |
|  8 | 2024-12-05 09:45:00+01:00 | 0 days 01:30:00 | Lecture  |
|  9 | 2024-12-12 08:00:00+01:00 | 0 days 01:30:00 | Exercise |
| 10 | 2024-12-12 09:45:00+01:00 | 0 days 01:30:00 | Lecture  |
| 11 | 2024-12-19 08:00:00+01:00 | 0 days 01:30:00 | Lecture  |
| 12 | 2024-12-19 09:45:00+01:00 | 0 days 01:30:00 | Lecture  |
| 13 | 2025-01-09 08:00:00+01:00 | 0 days 01:30:00 | Exercise |
| 14 | 2025-01-09 09:45:00+01:00 | 0 days 01:30:00 | Lecture  |
| 15 | 2025-01-16 08:00:00+01:00 | 0 days 01:30:00 | Exercise |
| 16 | 2025-01-16 09:45:00+01:00 | 0 days 01:30:00 | Lecture  |
| 17 | 2025-01-30 08:00:00+01:00 | 0 days 01:30:00 | Lecture  |
| 18 | 2025-01-30 09:45:00+01:00 | 0 days 01:30:00 | Exercise |
| 19 | 2025-02-06 08:00:00+01:00 | 0 days 01:30:00 | Lecture  |
| 20 | 2025-02-06 09:45:00+01:00 | 0 days 01:30:00 | Lecture  |
| 21 | 2025-02-13 08:00:00+01:00 | 0 days 01:30:00 | Exercise |
""".strip()
    assert actual == expected, "File content does not match the expected content"
