import { useState } from "react";
import "./App.css";

function App() {
  const [jdText, setJdText] = useState("");
  const [jdFile, setJdFile] = useState(null);
  const [resumeFiles, setResumeFiles] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [expandedCandidate, setExpandedCandidate] = useState(null);

  const handleAnalyze = async () => {
    if (!jdText.trim() && !jdFile) {
      setError(
        "Please type/paste a Job Description or upload a JD file."
      );
      return;
    }

    if (resumeFiles.length === 0) {
      setError("Please select at least one resume.");
      return;
    }

    setLoading(true);
    setError("");
    setResults([]);
    setExpandedCandidate(null);

    const formData = new FormData();

    if (jdText.trim()) {
      formData.append("jd_text", jdText);
    }

    if (jdFile) {
      formData.append("jd_file", jdFile);
    }

    resumeFiles.forEach((file) => {
      formData.append("resumes", file);
    });

    try {
      const response = await fetch(
        "http://127.0.0.1:8001/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data = await response.json();

      setResults(data.candidates || []);
    } catch (error) {
      setError(
        "Unable to connect to the backend. Make sure FastAPI is running on port 8001."
      );
    } finally {
      setLoading(false);
    }
  };

  const toggleCandidate = (candidateId) => {
    setExpandedCandidate(
      expandedCandidate === candidateId
        ? null
        : candidateId
    );
  };

  return (
    <div className="app">

      {/* HEADER */}

      <header className="header">
        <div className="header-content">

          <div>
            <h1>
              Resume Ranking System
            </h1>

            <p>
              Recruiter Dashboard for Resume Screening
            </p>
          </div>

        </div>
      </header>


      {/* MAIN */}

      <main className="container">

        {/* UPLOAD CARD */}

        <section className="upload-section">

          <h2>
            Analyze Candidates
          </h2>

          <p className="description">
            Enter a Job Description and upload candidate resumes
            to compare their skills and rank them.
          </p>


          {/* JOB DESCRIPTION */}

          <div className="upload-box">

            <label>
              Job Description
            </label>

            <textarea
              value={jdText}
              onChange={(event) => {

                setJdText(
                  event.target.value
                );

                setError("");

              }}
              placeholder={`Example:

Role: Frontend Developer

Required Skills:
React
JavaScript
HTML
CSS
REST API
Git

Preferred Skills:
AWS
Docker

Experience:
2 years

Education:
B.Tech / B.E / B.Sc in Computer Science`}
              rows="12"
            />

            <p className="input-hint">
              Type or paste today's Job Description here.
            </p>

          </div>


          {/* JD FILE */}

          <div className="upload-box">

            <label>
              Or Upload Job Description File
            </label>

            <input
              type="file"
              accept=".txt,.pdf,.doc,.docx"
              onChange={(event) => {

                setJdFile(
                  event.target.files[0] || null
                );

                setError("");

              }}
            />

            {jdFile && (

              <p className="file-name">
                Selected JD: {jdFile.name}
              </p>

            )}

          </div>


          {/* RESUMES */}

          <div className="upload-box">

            <label>
              Candidate Resumes
            </label>

            <input
              type="file"
              accept=".pdf"
              multiple
              onChange={(event) => {

                setResumeFiles(
                  Array.from(
                    event.target.files
                  )
                );

                setError("");

              }}
            />

            {resumeFiles.length > 0 && (

              <p className="file-name">
                {resumeFiles.length} resume(s) selected
              </p>

            )}

          </div>


          {/* ERROR */}

          {error && (

            <p className="error">
              {error}
            </p>

          )}


          {/* BUTTON */}

          <button
            className="analyze-button"
            onClick={handleAnalyze}
            disabled={loading}
          >

            {loading
              ? "Analyzing..."
              : "Analyze Resumes"}

          </button>

        </section>


        {/* RESULTS */}

        {results.length > 0 && (

          <section className="results-section">

            {/* RESULTS HEADER */}

            <div className="results-header">

              <div>

                <h2>
                  Candidate Ranking
                </h2>

                <p>
                  {results.length} candidate(s) analyzed
                </p>

              </div>

            </div>


            {/* RANKING TABLE */}

            <div className="table-container">

              <table>

                <thead>

                  <tr>

                    <th>
                      Rank
                    </th>

                    <th>
                      Candidate ID
                    </th>

                    <th>
                      Candidate
                    </th>

                    <th>
                      Resume
                    </th>

                    <th>
                      Required
                    </th>

                    <th>
                      Preferred
                    </th>

                    <th>
                      Overall Match
                    </th>

                    <th>
                      Experience
                    </th>

                    <th>
                      Education
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {results.map(
                    (candidate, index) => (

                      <tr key={index}>

                        <td>
                          <strong>
                            #{candidate.rank}
                          </strong>
                        </td>

                        <td>
                          <strong>
                            {candidate.candidate_id}
                          </strong>
                        </td>

                        <td>
                          <strong>
                            {candidate.candidate}
                          </strong>
                        </td>

                        <td>
                          {candidate.resume}
                        </td>

                        <td>
                          {candidate.required_score}%
                        </td>

                        <td>
                          {candidate.preferred_score}%
                        </td>

                        <td>
                          <strong className="score">
                            {candidate.overall_score}%
                          </strong>
                        </td>

                        <td>
                          {candidate.experience.status}
                        </td>

                        <td>
                          {candidate.education.status}
                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>


            {/* REQUIREMENT DETAILS */}

            <div className="details">

              <h2>
                Requirement Details
              </h2>

              <div className="candidate-cards">

                {results.map(
                  (candidate, candidateIndex) => {

                    const isExpanded =
                      expandedCandidate ===
                      candidate.candidate_id;

                    return (

                      <div
                        className={
                          isExpanded
                            ? "candidate-card expanded"
                            : "candidate-card"
                        }
                        key={candidateIndex}
                      >

                        {/* CARD HEADER */}

                        <div
                          className="candidate-card-header"
                          onClick={() =>
                            toggleCandidate(
                              candidate.candidate_id
                            )
                          }
                        >

                          <div className="candidate-main">

                            <div className="rank-badge">
                              #{candidate.rank}
                            </div>

                            <div>

                              <h3>
                                {candidate.candidate}
                              </h3>

                              <p>
                                {candidate.candidate_id}
                                {" • "}
                                {candidate.resume}
                              </p>

                            </div>

                          </div>


                          {/* SCORE SUMMARY */}

                          <div className="candidate-summary">

                            <div>
                              <span>
                                Required
                              </span>

                              <strong>
                                {candidate.required_score}%
                              </strong>
                            </div>


                            <div>
                              <span>
                                Preferred
                              </span>

                              <strong>
                                {candidate.preferred_score}%
                              </strong>
                            </div>


                            <div>
                              <span>
                                Overall
                              </span>

                              <strong className="overall-score">
                                {candidate.overall_score}%
                              </strong>
                            </div>


                            <div className="expand-icon">
                              {isExpanded ? "▲" : "▼"}
                            </div>

                          </div>

                        </div>


                        {/* EXPANDED DETAILS */}

                        {isExpanded && (

                          <div className="candidate-card-details">

                            {/* EXPERIENCE + EDUCATION */}

                            <div className="info-row">

                              <div className="info-item">

                                <span>
                                  Experience
                                </span>

                                <strong>
                                  {candidate.experience.status}
                                </strong>

                              </div>


                              <div className="info-item">

                                <span>
                                  Education
                                </span>

                                <strong>
                                  {candidate.education.status}
                                </strong>

                              </div>

                            </div>


                            {/* REQUIRED */}

                            <div className="skill-section">

                              <h4>
                                Required Skills
                              </h4>

                              <div className="skill-grid">

                                {candidate.required.map(
                                  (item, index) => (

                                    <div
                                      className="skill-item"
                                      key={index}
                                    >

                                      <div className="skill-name">
                                        {item.requirement}
                                      </div>

                                      <span
                                        className={
                                          item.status === "MATCHED"
                                            ? "status matched"
                                            : item.status === "RELATED"
                                            ? "status related"
                                            : "status missing"
                                        }
                                      >
                                        {item.status}
                                      </span>

                                      {item.evidence && (

                                        <small>
                                          Evidence:{" "}
                                          {item.evidence}
                                        </small>

                                      )}

                                    </div>

                                  )
                                )}

                              </div>

                            </div>


                            {/* PREFERRED */}

                            <div className="skill-section">

                              <h4>
                                Preferred Skills
                              </h4>

                              <div className="skill-grid">

                                {candidate.preferred.map(
                                  (item, index) => (

                                    <div
                                      className="skill-item"
                                      key={index}
                                    >

                                      <div className="skill-name">
                                        {item.requirement}
                                      </div>

                                      <span
                                        className={
                                          item.status === "MATCHED"
                                            ? "status matched"
                                            : item.status === "RELATED"
                                            ? "status related"
                                            : "status missing"
                                        }
                                      >
                                        {item.status}
                                      </span>

                                      {item.evidence && (

                                        <small>
                                          Evidence:{" "}
                                          {item.evidence}
                                        </small>

                                      )}

                                    </div>

                                  )
                                )}

                              </div>

                            </div>

                          </div>

                        )}

                      </div>

                    );

                  }
                )}

              </div>

            </div>

          </section>

        )}

      </main>

    </div>
  );
}

export default App;
