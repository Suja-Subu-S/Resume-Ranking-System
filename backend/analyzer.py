from jd_parser import extract_requirements_from_jd
from resume_parser import extract_text_from_resume
from matcher import match_requirements_with_resume


# ==========================================
# SAMPLE JOB DESCRIPTION
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
# PARSE JOB DESCRIPTION
# ==========================================

requirements = extract_requirements_from_jd(
    jd_text
)


# ==========================================
# LOAD RESUME PDF
# ==========================================

file_path = "__SUJA S__.pdf"

resume_text = extract_text_from_resume(
    file_path
)


# ==========================================
# MATCH RESUME WITH JOB DESCRIPTION
# ==========================================

result = match_requirements_with_resume(
    requirements,
    resume_text
)


# ==========================================
# DISPLAY JOB REQUIREMENTS
# ==========================================

print("\n========================================")
print("JOB REQUIREMENTS")
print("========================================")


print("\nRequired Skills:")

for skill in requirements["required"]:

    print("-", skill)


print("\nPreferred Skills:")

for skill in requirements["preferred"]:

    print("-", skill)


print("\nExperience:")
print(requirements["experience"])


print("\nEducation:")
print(requirements["education"])


# ==========================================
# DISPLAY MATCHING RESULTS
# ==========================================

print("\n========================================")
print("RESUME MATCHING RESULTS")
print("========================================")


# ==========================================
# REQUIRED SKILLS
# ==========================================

print("\n===== REQUIRED SKILLS =====")


for item in result["required"]:

    print(

        item["requirement"],

        "->",

        item["status"],

        "| Evidence:",

        item["evidence"]

    )


# ==========================================
# PREFERRED SKILLS
# ==========================================

print("\n===== PREFERRED SKILLS =====")


for item in result["preferred"]:

    print(

        item["requirement"],

        "->",

        item["status"],

        "| Evidence:",

        item["evidence"]

    )


# ==========================================
# EXPERIENCE
# ==========================================

print("\n===== EXPERIENCE =====")


print(

    result["experience"]["requirement"],

    "->",

    result["experience"]["status"]

)


# ==========================================
# EDUCATION
# ==========================================

print("\n===== EDUCATION =====")


print(

    result["education"]["requirement"],

    "->",

    result["education"]["status"]

)


# ==========================================
# MATCH SCORES
# ==========================================

print("\n========================================")
print("MATCH SCORES")
print("========================================")


print(

    "Required Score:",

    result["required_score"],

    "%"

)


print(

    "Preferred Score:",

    result["preferred_score"],

    "%"

)


print(

    "Overall Score:",

    result["overall_score"],

    "%"

)
