import os
import re
import subprocess
import sys
from itertools import count
from time import sleep

import docx
from docx2pdf import convert
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, RGBColor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from dice import Dice


def convert_to_pdf(input_docx, out_folder):
    args = [
        libreoffice_exec(),
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        out_folder,
        input_docx,
    ]

    process = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15
    )
    filename = re.search("-> (.*?) using filter", process.stdout.decode())

    return filename.group(1)


def libreoffice_exec():
    # TODO: Provide support for more platforms
    if sys.platform == "darwin":
        return "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    return "libreoffice"


def get_skills_text(description):
    text = description.split("Job Description")
    text = "".join(text).split("Report this job")[0]

    # Create a regular expression pattern using the characters to replace
    pattern = r"\b[A-Z][a-zA-Z]*\b"
    # Replace the characters using the sub() function
    result = re.findall(pattern, text)
    result = " ".join(result)
    print("\nSTRING TO APPEND")
    print(result)
    print("\n")
    return result


def main(description):
    doc_url = "/Users/gauravshilpakar/Desktop/Clicker/Dice/resume/ORIGINAL RESUME.docx"
    doc = docx.Document(doc_url)

    # Get the last paragraph in the document
    last_paragraph = doc.add_paragraph(get_skills_text(description))

    # Apply formatting to the last paragraph
    for run in last_paragraph.runs:
        run.font.size = Pt(1)  # Change font size to 0 points
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.bold = False

    print("Saving DOCX")
    doc.save("./resume/Gaurav Shilpakar - Resume 2023.docx")
    sample_doc = "./resume/Gaurav Shilpakar - Resume 2023.docx"
    out_folder = "./resume/"
    print("Saving PDF")
    convert_to_pdf(sample_doc, out_folder)


dice = Dice(
    "gaurav.shilpakar2054@gmail.com",
    "Gaurav5555!",
    "ANGULAR BACKEND FRONTEND SOFTWARE ENGINEER DEVELOPER CONTRACT C2C",
    "",
    "/Users/gauravshilpakar/Desktop/Clicker/Dice/AGaurav Shilpakar - Resume 2023.docx.pdf",
    "",
    5,
)
