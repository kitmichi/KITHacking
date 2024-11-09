import tempfile
from collections import Counter
from pathlib import Path

import pandas as pd
import pypdf2htmlEX
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from table_math.find_min_distances import find_mins, print_mins


# Function to convert PDF to HTML while preserving layout
def pdf_to_html_preserve_layout(pdf_path: Path, html_path: Path):
    # Convert PDF to HTML
    pdf = pypdf2htmlEX.PDF(pdf_path)
    pdf.to_html(dest_dir=html_path.parent, new_file_name=html_path.name)


def get_absolute_positions(htmlPath: Path):
    # Set up the WebDriver (assuming ChromeDriver is in the PATH)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    # Open the HTML file in the browser
    driver.get(f"file://{htmlPath.absolute()}")

    # Find all div elements with class "c"
    divs = driver.find_elements(By.CSS_SELECTOR, "div.c")

    positions = []
    for div in divs:
        text = div.text.strip()
        x = div.location["x"]
        y = div.location["y"]
        width = div.size["width"]
        height = div.size["height"]

        positions.append(
            {"text": text, "x": x, "y": y, "width": width, "height": height}
        )

    driver.quit()
    return positions


def filter_table_cells(positions):
    # Count occurrences of x and width combinations and y and height combinations
    x_width_counter = Counter((pos["x"], pos["width"]) for pos in positions)
    y_height_counter = Counter((pos["y"], pos["height"]) for pos in positions)

    # Filter positions based on the counts
    filtered_positions = [
        pos
        for pos in positions
        if x_width_counter[(pos["x"], pos["width"])] > 2
        or y_height_counter[(pos["y"], pos["height"])] > 2
    ]

    return filtered_positions


def create_table(positions):
    # Create a DataFrame from the positions
    df = pd.DataFrame(positions)

    # Pivot the DataFrame to create a table
    table = df.pivot(index="y", columns="x", values="text")

    return table


def extract_table(pdf_path: Path):
    # Create a temporary directory
    with tempfile.TemporaryDirectory(dir=pdf_path.parent) as temp_dir:
        html_path = Path(temp_dir) / pdf_path.with_suffix(".html").name

        pdf_to_html_preserve_layout(pdf_path, html_path)

        positions = get_absolute_positions(html_path)
    filtered_positions = filter_table_cells(positions)
    print_mins(find_mins(filtered_positions))
    return create_table(filtered_positions)
