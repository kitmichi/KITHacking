import os
from collections import Counter
from pathlib import Path

import pandas as pd
import pypdf2htmlEX
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# Function to convert PDF to HTML while preserving layout
def pdf_to_html_preserve_layout(pdfPath: Path):
    # Get the current directory of the script

    # Convert PDF to HTML
    pdf = pypdf2htmlEX.PDF(pdfPath)
    htmlPath = pdfPath.with_suffix(".html")
    pdf.to_html(dest_dir=pdfPath.parent, new_file_name=htmlPath.name)
    return htmlPath


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

    # Round the y positions to group them into rows
    df["y"] = df["y"].round(-1)

    # Pivot the DataFrame to create a table
    table = df.pivot(index="y", columns="x", values="text")

    return table


def generate_pmwiki_table(table):
    for irow in range(table.shape[0]):
        for icol in range(table.shape[1]):
            if irow < 2:
                if pd.isna(table.iloc[irow, icol]):
                    continue
                if icol == 0:
                    table.iloc[irow, icol] = f"!{table.iloc[irow, icol]} "
                else:
                    table.iloc[irow, icol] = f"! {table.iloc[irow, icol]} "
            else:
                if pd.isna(table.iloc[irow, icol]):
                    continue
                if icol == 0:
                    table.iloc[irow, icol] = f"{table.iloc[irow, icol]} "
                else:
                    table.iloc[irow, icol] = f" {table.iloc[irow, icol]} "

    pmwiki_table = "|| border=1\n"

    # Calculate the maximum length of each column for alignment
    col_max_lengths = (
        table.map(lambda x: len(str(x)) if not pd.isna(x) else 0).max().to_dict()
    )

    for irow, row in zip(range(table.shape[0]), table.index):
        for col in table.columns:
            if pd.isna(table.loc[row, col]):
                pmwiki_table += " " * (col_max_lengths[col]) + "||"
                continue
            cell_content = str(table.loc[row, col])
            cell_content += " " * (col_max_lengths[col] - len(cell_content))
            pmwiki_table += f"||{cell_content}"
        pmwiki_table += "||\n"

    return pmwiki_table


class PdfModulesExtractor:
    def __init__(self, base_dir: Path = Path(__file__).parent):
        self.base_dir = base_dir

    def get_pdf(self):
        url = (
            "https://www.etit.kit.edu/rd_download/SGS/ETIT/"
            "empfohlene%20Wahlmodule/VR09_empfohlene_Wahlmodule.pdf"
        )
        filename = os.path.basename(url)
        pdfPath = self.base_dir / filename

        response = requests.get(url)
        with open(pdfPath, "wb") as file:
            file.write(response.content)

        print(f"PDF saved to {pdfPath}")
        return pdfPath

    def main(self):
        # Example usage
        pdfPath = self.get_pdf()

        # Convert the provided PDF file to HTML
        htmlPath = pdf_to_html_preserve_layout(pdfPath)

        print(
            f"The PDF has been successfully converted to HTML and saved as "
            f"'{htmlPath}'."
        )

        positions = get_absolute_positions(htmlPath)
        filtered_positions = filter_table_cells(positions)
        table = create_table(filtered_positions)

        # Generate pmwiki table
        pmwiki_table = generate_pmwiki_table(table)

        # Print the pmwiki table
        print(pmwiki_table)

        # Optionally, save the pmwiki table to a text file
        pmwiki_file = htmlPath.with_suffix(".pmwiki")
        with open(pmwiki_file, "w") as f:
            f.write(pmwiki_table)
        print(f"pmwiki file storad at '{pmwiki_file}'")


if __name__ == "__main__":
    PdfModulesExtractor().main()
