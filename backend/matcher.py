import re


# ---------------------------------------------------------
# SKILL ALIASES
# ---------------------------------------------------------

SKILL_ALIASES = {

    "rest api": [
        "rest api",
        "restful api",
        "restful apis",
        "rest services",
        "restful web services"
    ],

    "javascript": [
        "javascript",
        "js"
    ],

    "machine learning": [
        "machine learning",
        "ml"
    ],

    "database": [
        "database",
        "databases"
    ]
}


# ---------------------------------------------------------
# CHECK WHETHER A SKILL EXISTS
# ---------------------------------------------------------

def contains_skill(skill, resume_text):

    pattern = r"\b" + re.escape(skill) + r"\b"

    return re.search(
        pattern,
        resume_text,
        re.IGNORECASE
    ) is not None


# ---------------------------------------------------------
# FIND EXACT EVIDENCE
# ---------------------------------------------------------

def find_exact_evidence(skill, resume_text):

    lines = resume_text.splitlines()

    for line in lines:

        if contains_skill(skill, line):

            return skill

    return None


# ---------------------------------------------------------
# FIND RELATED EVIDENCE
# ---------------------------------------------------------

def find_related_evidence(skill, resume_text):

    skill_lower = skill.lower()

    aliases = SKILL_ALIASES.get(
        skill_lower,
        []
    )

    for alias in aliases:

        if contains_skill(
            alias,
            resume_text
        ):

            return alias

    return None


# ---------------------------------------------------------
# MATCH SKILL
# ---------------------------------------------------------

def match_skill(skill, resume_text):

    exact_evidence = find_exact_evidence(
        skill,
        resume_text
    )

    if exact_evidence:

        return {
            "status": "MATCHED",
            "evidence": exact_evidence
        }


    related_evidence = find_related_evidence(
        skill,
        resume_text
    )

    if related_evidence:

        return {
            "status": "RELATED",
            "evidence": related_evidence
        }


    return {
        "status": "MISSING",
        "evidence": None
    }


# ---------------------------------------------------------
# MATCH EXPERIENCE
# ---------------------------------------------------------

def match_experience(
    experience_requirement,
    resume_text
):

    if not experience_requirement:

        return {
            "requirement": None,
            "status": "UNCLEAR"
        }


    experience_keywords = [

        "experience",
        "internship",
        "intern",
        "fresher",
        "years"

    ]


    for keyword in experience_keywords:

        if re.search(
            r"\b" + re.escape(keyword) + r"\b",
            resume_text,
            re.IGNORECASE
        ):

            return {
                "requirement":
                    experience_requirement,

                "status":
                    "MATCHED"
            }


    return {
        "requirement":
            experience_requirement,

        "status":
            "UNCLEAR"
    }


# ---------------------------------------------------------
# MATCH EDUCATION
# ---------------------------------------------------------

def match_education(
    education_requirement,
    resume_text
):

    if not education_requirement:

        return {
            "requirement": None,
            "status": "UNCLEAR"
        }


    education_keywords = [

        "b.tech",
        "b.e",
        "bachelor",
        "engineering",
        "computer science",
        "computer and business systems",
        "csbs"

    ]


    for keyword in education_keywords:

        if contains_skill(
            keyword,
            resume_text
        ):

            return {
                "requirement":
                    education_requirement,

                "status":
                    "MATCHED"
            }


    return {
        "requirement":
            education_requirement,

        "status":
            "MISSING"
    }


# ---------------------------------------------------------
# MATCH ALL REQUIREMENTS
# ---------------------------------------------------------

def match_requirements_with_resume(
    requirements,
    resume_text
):

    result = {

        "required": [],

        "preferred": [],

        "experience": {},

        "education": {},

        "required_score": 0,

        "preferred_score": 0,

        "overall_score": 0

    }


    # -----------------------------------------------------
    # REQUIRED SKILLS
    # -----------------------------------------------------

    required_matched = 0


    for skill in requirements["required"]:

        match = match_skill(
            skill,
            resume_text
        )


        if match["status"] in [
            "MATCHED",
            "RELATED"
        ]:

            required_matched += 1


        result["required"].append({

            "requirement":
                skill,

            "status":
                match["status"],

            "evidence":
                match["evidence"]

        })


    total_required = len(
        requirements["required"]
    )


    if total_required > 0:

        result["required_score"] = (

            required_matched
            / total_required

        ) * 100


    # -----------------------------------------------------
    # PREFERRED SKILLS
    # -----------------------------------------------------

    preferred_matched = 0


    for skill in requirements["preferred"]:

        match = match_skill(
            skill,
            resume_text
        )


        if match["status"] in [
            "MATCHED",
            "RELATED"
        ]:

            preferred_matched += 1


        result["preferred"].append({

            "requirement":
                skill,

            "status":
                match["status"],

            "evidence":
                match["evidence"]

        })


    total_preferred = len(
        requirements["preferred"]
    )


    if total_preferred > 0:

        result["preferred_score"] = (

            preferred_matched
            / total_preferred

        ) * 100


    # -----------------------------------------------------
    # EXPERIENCE
    # -----------------------------------------------------

    result["experience"] = match_experience(

        requirements.get("experience"),

        resume_text

    )


    # -----------------------------------------------------
    # EDUCATION
    # -----------------------------------------------------

    result["education"] = match_education(

        requirements.get("education"),

        resume_text

    )


    # -----------------------------------------------------
    # OVERALL SCORE
    # -----------------------------------------------------

    total_requirements = (

        total_required
        + total_preferred

    )


    total_matched = (

        required_matched
        + preferred_matched

    )


    if total_requirements > 0:

        result["overall_score"] = (

            total_matched
            / total_requirements

        ) * 100


    return result
