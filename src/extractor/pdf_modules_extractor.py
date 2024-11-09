import os
from pathlib import Path

import pandas as pd
import requests

from .pdf_table_extractor import extract_table


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

        table = extract_table(pdfPath)

        # Generate pmwiki table
        pmwiki_table = generate_pmwiki_table(table)

        # Print the pmwiki table
        print(pmwiki_table)

        # Optionally, save the pmwiki table to a text file
        pmwiki_file = pdfPath.with_suffix(".pmwiki")
        with open(pmwiki_file, "w") as f:
            f.write(pmwiki_table)
        print(f"pmwiki file storad at '{pmwiki_file}'")


if __name__ == "__main__":
    PdfModulesExtractor().main()
