import os
import pdfplumber
from docx import Document


def extract_text_from_pdf(file_path):
    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_text_from_txt(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        return file.read()


def extract_text_from_docx(file_path):

    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text += paragraph.text + "\n"

    return text


def extract_text_from_file(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":

        return extract_text_from_pdf(
            file_path
        )

    elif extension == ".txt":

        return extract_text_from_txt(
            file_path
        )

    elif extension == ".docx":

        return extract_text_from_docx(
            file_path
        )

    else:

        raise ValueError(
            "Unsupported file type: "
            + extension
        )


# Keep the old function name
# so existing code continues to work.

def extract_text_from_resume(file_path):

    return extract_text_from_file(
        file_path
    )


def extract_candidate_name(resume_text):
    """
    Extract candidate name from the first few
    meaningful lines of the resume.
    """

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    if not lines:
        return "Unknown Candidate"

    # Check the first few lines
    # for a likely candidate name.

    for line in lines[:8]:

        ignored_words = [
            "resume",
            "curriculum vitae",
            "cv",
            "profile",
            "contact",
            "email",
            "phone",
            "mobile"
        ]

        if line.lower() in ignored_words:
            continue

        # Ignore contact information

        if "@" in line:
            continue

        # Ignore lines containing numbers

        if any(char.isdigit() for char in line):
            continue

        # Avoid very long lines

        if len(line.split()) > 5:
            continue

        return line

    return "Unknown Candidate"
