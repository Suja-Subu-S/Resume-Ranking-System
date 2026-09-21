 Resume Ranking System

A full-stack web application that analyzes resumes against a given job description and ranks candidates based on how closely their skills and experience match the job requirements.

 Features

* Upload a Job Description
* Upload multiple candidate resumes
* Extract text from resumes
* Parse job description requirements
* Analyze candidate skills and qualifications
* Calculate resume-to-job matching scores
* Rank candidates based on their matching scores
* Display analysis results through a web interface

 🛠️ Technologies Used

 Frontend

* React.js
* Vite
* HTML
* CSS
* JavaScript

 Backend

* Python
* FastAPI

 Resume & Job Description Processing

* Python-based text extraction
* Resume parsing
* Job description parsing
* Skill matching and analysis

 Development Tools

* Visual Studio Code
* Git
* Github

 Project Structure

Resume-Ranking-System/
│
├── backend/
│   ├── analyzer.py
│   ├── batch_analyzer.py
│   ├── jd_parser.py
│   ├── main.py
│   ├── matcher.py
│   ├── resume_parser.py
│   ├── sample_jd.txt
│   └── test_parser.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

 🔄 Application Workflow

```text
Job Description
       ↓
Upload JD
       ↓
Resume Upload
       ↓
Resume Text Extraction
       ↓
Job Description Parsing
       ↓
Skill & Requirement Matching
       ↓
Candidate Score Calculation
       ↓
Candidate Ranking
       ↓
Display Results

🎯 Purpose

The purpose of this project is to simplify the initial resume screening process by automatically comparing candidate resumes with job descriptions and providing a ranked list of candidates based on their relevance to the specified role.

 Author
Suja S

GitHub: [Suja-Subu-S](https://github.com/Suja-Subu-S)
