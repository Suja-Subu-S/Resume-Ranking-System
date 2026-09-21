import os

from jd_parser import extract_requirements_from_jd
from resume_parser import extract_text_from_resume
from matcher import match_requirements_with_resume


# ==========================================
# JOB DESCRIPTION
# ==========================================

jd_text = """
We are looking for a Java Software Developer.

Required Skills:
Java, Spring Boot, SQL, REST API, Git

Preferred Skills:
Docker, AWS, React

Experience:
0-2 years

Education:
B.Tech / B.E in Computer Science or related field
"""


# ==========================================
# RESUME FOLDER
# ==========================================

resume_folder = "."


# ==========================================
# PARSE JOB DESCRIPTION
# ==========================================

requirements = extract_requirements_from_jd(
    jd_text
)


# ==========================================
# FIND ALL PDF RESUMES
# ==========================================

resume_files = []

for file_name in os.listdir(resume_folder):

    if file_name.lower().endswith(".pdf"):

        resume_files.append(file_name)


# ==========================================
# CHECK WHETHER RESUMES EXIST
# ==========================================

if not resume_files:

    print("No PDF resumes found.")

    exit()


# ==========================================
# ANALYZE ALL RESUMES
# ==========================================

all_results = []


for resume_file in resume_files:

    print("\n========================================")
    print("ANALYZING:", resume_file)
    print("========================================")


    # Resume path
    file_path = os.path.join(
        resume_folder,
        resume_file
    )


    # Extract resume text
    resume_text = extract_text_from_resume(
        file_path
    )


    # Match resume with JD
    result = match_requirements_with_resume(

        requirements,

        resume_text

    )


    # Store result
    all_results.append({

        "resume": resume_file,

        "result": result

    })


    # ==========================================
    # DISPLAY REQUIRED SKILLS
    # ==========================================

    print("\nRequired Skills:")


    for item in result["required"]:

        print(

            item["requirement"],

            "->",

            item["status"]

        )


    # ==========================================
    # DISPLAY PREFERRED SKILLS
    # ==========================================

    print("\nPreferred Skills:")


    for item in result["preferred"]:

        print(

            item["requirement"],

            "->",

            item["status"]

        )


    # ==========================================
    # DISPLAY EXPERIENCE
    # ==========================================

    print("\nExperience:")

    print(

        result["experience"]["requirement"],

        "->",

        result["experience"]["status"]

    )


    # ==========================================
    # DISPLAY EDUCATION
    # ==========================================

    print("\nEducation:")

    print(

        result["education"]["requirement"],

        "->",

        result["education"]["status"]

    )


    # ==========================================
    # DISPLAY SCORE
    # ==========================================

    print("\nOverall Score:")

    print(

        result["overall_score"],

        "%"

    )


# ==========================================
# SORT CANDIDATES BY SCORE
# ==========================================

all_results.sort(

    key=lambda item: item["result"]["overall_score"],

    reverse=True

)


# ==========================================
# FINAL CANDIDATE RANKING
# ==========================================

print("\n\n========================================")
print("CANDIDATE RANKING")
print("========================================")


rank = 1


for item in all_results:

    print(

        rank,

        ".",

        item["resume"],

        "->",

        item["result"]["overall_score"],

        "%"

    )

    rank += 1
