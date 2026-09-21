def extract_requirements_from_jd(jd_text):
    requirements = {
        "required": [],
        "preferred": [],
        "experience": None,
        "education": None
    }

    lines = jd_text.strip().splitlines()

    current_section = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.lower() == "required skills:":
            current_section = "required"
            continue

        if line.lower() == "preferred skills:":
            current_section = "preferred"
            continue

        if line.lower() == "experience:":
            current_section = "experience"
            continue

        if line.lower() == "education:":
            current_section = "education"
            continue

        if current_section == "required":
            skills = line.split(",")

            for skill in skills:
                skill = skill.strip()

                if skill:
                    requirements["required"].append(skill)

        elif current_section == "preferred":
            skills = line.split(",")

            for skill in skills:
                skill = skill.strip()

                if skill:
                    requirements["preferred"].append(skill)

        elif current_section == "experience":
            requirements["experience"] = line
            current_section = None

        elif current_section == "education":
            requirements["education"] = line
            current_section = None

    return requirements


# Sample Job Description
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


# Extract requirements
result = extract_requirements_from_jd(jd_text)

