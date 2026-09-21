from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import shutil
import uuid

from jd_parser import extract_requirements_from_jd
from resume_parser import (
    extract_text_from_file,
    extract_candidate_name
)
from matcher import match_requirements_with_resume


app = FastAPI(
    title="Resume Ranking System"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Resume Ranking System API is running!"
    }


# ---------------------------------------------------------
# ANALYZE RESUMES
# ---------------------------------------------------------

@app.post("/analyze")
async def analyze_resumes(

    # Optional JD file
    jd_file: Optional[UploadFile] = File(None),

    # Optional typed/pasted JD
    jd_text: Optional[str] = Form(None),

    # Multiple resumes
    resumes: List[UploadFile] = File(...)

):

    # -----------------------------------------------------
    # Validate JD
    # -----------------------------------------------------

    if not jd_text and not jd_file:

        return {
            "message": "Please provide a Job Description."
        }


    # -----------------------------------------------------
    # Temporary folder
    # -----------------------------------------------------

    temp_folder = "temp_resumes"

    os.makedirs(
        temp_folder,
        exist_ok=True
    )


    # -----------------------------------------------------
    # Get JD text
    # -----------------------------------------------------

    if jd_text and jd_text.strip():

        jd_content = jd_text.strip()

    else:

        unique_jd_name = (
            "job_description_"
            + str(uuid.uuid4())
            + "_"
            + jd_file.filename
        )

        jd_path = os.path.join(
            temp_folder,
            unique_jd_name
        )

        with open(jd_path, "wb") as file:

            shutil.copyfileobj(
                jd_file.file,
                file
            )

        jd_content = extract_text_from_file(
            jd_path
        )


    # -----------------------------------------------------
    # Parse JD
    # -----------------------------------------------------

    requirements = extract_requirements_from_jd(
        jd_content
    )


    # -----------------------------------------------------
    # Analyze every resume
    # -----------------------------------------------------

    all_results = []


    for index, resume in enumerate(
        resumes,
        start=1
    ):

        # -------------------------------------------------
        # Create unique internal filename
        # -------------------------------------------------

        unique_resume_name = (
            str(uuid.uuid4())
            + "_"
            + resume.filename
        )

        resume_path = os.path.join(
            temp_folder,
            unique_resume_name
        )


        # -------------------------------------------------
        # Save resume
        # -------------------------------------------------

        with open(resume_path, "wb") as file:

            shutil.copyfileobj(
                resume.file,
                file
            )


        # -------------------------------------------------
        # Extract resume text
        # -------------------------------------------------

        resume_text = extract_text_from_file(
            resume_path
        )


        # -------------------------------------------------
        # Extract candidate name
        # -------------------------------------------------

        candidate_name = extract_candidate_name(
            resume_text
        )


        # -------------------------------------------------
        # Match requirements
        # -------------------------------------------------

        result = match_requirements_with_resume(
            requirements,
            resume_text
        )


        # -------------------------------------------------
        # Create unique candidate ID
        # -------------------------------------------------

        candidate_id = (
            "CAND-"
            + str(index).zfill(3)
        )


        # -------------------------------------------------
        # Store result
        # -------------------------------------------------

        all_results.append({

            # Unique candidate ID
            "candidate_id":
                candidate_id,

            # Actual candidate name
            "candidate":
                candidate_name,

            # Original resume filename
            "resume":
                resume.filename,

            "overall_score":
                result["overall_score"],

            "required_score":
                result["required_score"],

            "preferred_score":
                result["preferred_score"],

            "required":
                result["required"],

            "preferred":
                result["preferred"],

            "experience":
                result["experience"],

            "education":
                result["education"]

        })


    # -----------------------------------------------------
    # Sort candidates by overall score
    # -----------------------------------------------------

    all_results.sort(
        key=lambda item:
            item["overall_score"],
        reverse=True
    )


    # -----------------------------------------------------
    # Assign ranking after sorting
    # -----------------------------------------------------

    for rank, candidate in enumerate(
        all_results,
        start=1
    ):

        candidate["rank"] = rank


    # -----------------------------------------------------
    # Return results
    # -----------------------------------------------------

    return {

        "message":
            "Analysis completed successfully",

        "total_candidates":
            len(all_results),

        "candidates":
            all_results

    }
