import inspect
import tempfile
from pathlib import Path

import fitz

import extractor.extract_events_EMNCF.create_events
from extractor.extract_events_EMNCF.create_events import write_files


def test():
    base_path = Path(
        inspect.getabsfile(extractor.extract_events_EMNCF.create_events)
    ).parent
    pdf_path = base_path / "EMNCF_00_Organization_Introduction_WS2024.pdf"
    page_number = 4
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_number)
    text = {}
    fitz_rect = {
        "Lecture": fitz.Rect(119.0, 156.0, 230.0, 508.0),
        "Exercise": fitz.Rect(484.0, 200.0, 592.0, 350.0),
    }
    with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp_dir:
        for key, rect in fitz_rect.items():
            text = page.get_textbox(rect).strip()
            with open(Path(temp_dir) / f"{key}.txt", "w") as f:
                f.write(text)
        tsv, ics, md = write_files(Path(temp_dir))
        file_content = md.read_text().strip()
    expected_content = """
|    | Weekday   | Date       | Time          | Event      |
|---:|:----------|:-----------|:--------------|:-----------|
|  0 | Thursday  | 31.10.2024 | 17:30 – 19:00 | Lecture 1  |
|  1 | Thursday  | 07.11.2024 | 17:30 – 19:00 | Lecture 2  |
|  2 | Thursday  | 14.11.2024 | 17:30 – 19:00 | Lecture 3  |
|  3 | Tuesday   | 19.11.2024 | 17:30 – 19:00 | Exercise 1 |
|  4 | Thursday  | 21.11.2024 | 17:30 – 19:00 | Lecture 4  |
|  5 | Thursday  | 28.11.2024 | 17:30 – 19:00 | Lecture 5  |
|  6 | Tuesday   | 03.12.2024 | 17:30 – 19:00 | Exercise 2 |
|  7 | Thursday  | 05.12.2024 | 17:30 – 19:00 | Lecture 6  |
|  8 | Thursday  | 12.12.2024 | 17:30 – 19:00 | Lecture 7  |
|  9 | Tuesday   | 17.12.2024 | 17:30 – 19:00 | Exercise 3 |
| 10 | Thursday  | 19.12.2024 | 17:30 – 19:00 | Lecture 8  |
| 11 | Tuesday   | 07.01.2025 | 17:30 – 19:00 | Exercise 4 |
| 12 | Thursday  | 09.01.2025 | 17:30 – 19:00 | Lecture 9  |
| 13 | Tuesday   | 14.01.2025 | 17:30 – 19:00 | Lecture 10 |
| 14 | Thursday  | 16.01.2025 | 17:30 – 19:00 | Lecture 11 |
| 15 | Tuesday   | 21.01.2025 | 17:30 – 19:00 | Exercise 5 |
| 16 | Thursday  | 30.01.2025 | 17:30 – 19:00 | Exercise 6 |
| 17 | Tuesday   | 04.02.2025 | 17:30 – 19:00 | Lecture 12 |
| 18 | Thursday  | 06.02.2025 | 17:30 – 19:00 | Lecture 13 |
| 19 | Thursday  | 13.02.2025 | 17:30 – 19:00 | Lecture 14 |
""".strip()

    # Assert that the file content matches the expected content
    assert (
        file_content == expected_content
    ), "File content does not match the expected content"
