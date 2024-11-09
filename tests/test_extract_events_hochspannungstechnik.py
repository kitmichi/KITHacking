import tempfile
from pathlib import Path

from extractor.extract_events_hochspannungstechnik import write_files


def test():
    temp_dir = tempfile.TemporaryDirectory(dir=str(Path(__file__).parent))
    base_path = Path(temp_dir.name)
    tsv, ics, md = write_files(
        base_path,
        (
            "https://ilias.studium.kit.edu/login.php?"
            "client_id=produktiv&cmd=force_login&lang=de"
        ),
    )
    expected_content = """
|   y | Weekday   | Date       | Time          | Event         |
|----:|:----------|:-----------|:--------------|:--------------|
| 240 | Montag    | 21.10.2024 | 14:00 – 15:30 | 1. Vorlesung  |
| 257 | Dienstag  | 22.10.2024 | 11:30 – 13:00 | 2. Vorlesung  |
| 275 | Montag    | 28.10.2024 | 14:00 – 15:30 | Übung 1       |
| 292 | Montag    | 04.11.2024 | 14:00 – 15:30 | 3. Vorlesung  |
| 310 | Dienstag  | 05.11.2024 | 11:30 – 13:00 | 4. Vorlesung  |
| 327 | Montag    | 11.11.2024 | 14:00 – 15:30 | Übung 2       |
| 345 | Dienstag  | 12.11.2024 | 11:30 – 13:00 | 5. Vorlesung  |
| 362 | Montag    | 18.11.2024 | 14:00 – 15:30 | Übung 3       |
| 380 | Dienstag  | 19.11.2024 | 11:30 – 13:00 | 6. Vorlesung  |
| 397 | Montag    | 25.11.2024 | 14:00 – 15:30 | Übung 4       |
| 415 | Dienstag  | 26.11.2024 | 11:30 – 13:00 | 7. Vorlesung  |
| 432 | Montag    | 02.12.2024 | 14:00 – 15:30 | Übung 5       |
| 450 | Dienstag  | 03.12.2024 | 11:30 – 13:00 | 8. Vorlesung  |
| 468 | Montag    | 09.12.2024 | 14:00 – 15:30 | Übung 6       |
| 485 | Dienstag  | 10.12.2024 | 11:30 – 13:00 | 9. Vorlesung  |
| 502 | Montag    | 16.12.2024 | 14:00 – 15:30 | Übung 7       |
| 520 | Dienstag  | 17.12.2024 | 11:30 – 13:00 | 10. Vorlesung |
| 537 | Dienstag  | 07.01.2025 | 11:30 – 13:00 | 11. Vorlesung |
| 555 | Montag    | 13.01.2025 | 14:00 – 15:30 | Übung 8       |
| 573 | Dienstag  | 14.01.2025 | 11:30 – 13:00 | 12. Vorlesung |
| 590 | Montag    | 20.01.2025 | 14:00 – 15:30 | Übung 9       |
| 607 | Dienstag  | 21.01.2025 | 11:30 – 13:00 | 13. Vorlesung |
| 625 | Montag    | 27.01.2025 | 14:00 – 15:30 | Übung 10      |
| 642 | Dienstag  | 28.01.2025 | 11:30 – 13:00 | Übung 11      |
| 660 | Montag    | 03.02.2025 | 14:00 – 15:30 | Übung 12      |
| 678 | Montag    | 10.02.2025 | 14:00 – 15:30 | Fragestunde   |
| 695 | Samstag   | 01.03.2025 | 09:00 – 11:00 | Klausur       |
""".strip()
    file_content = md.read_text().strip()

    # Assert that the file content matches the expected content
    assert (
        file_content == expected_content
    ), "File content does not match the expected content"
