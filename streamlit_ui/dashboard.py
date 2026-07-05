import streamlit as st   # Streamlit is the framework that builds the entire web UI
import sys               # sys is used to modify the Python module search path
import os                # os is used for file and folder operations
import tempfile          # tempfile creates temporary files to save uploaded PDFs before reading them

# Add the project root folder to Python's path so we can import from the src folder
# Without this, imports like "from src.parser..." would fail since we are inside streamlit_ui/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parser.pdf_parser import extract_text_from_pdf      # Reads a PDF and returns all its text
from src.llm.extractor import extract_document_data          # Uses LLM to extract skills and experience from text
from src.llm.skill_matcher import llm_skill_match            # Uses LLM to match resume skills against JD skills
from src.matcher.embedding_matcher import generate_embedding  # Converts text into a vector for similarity search
from src.matcher.vector_store import index_job_descriptions, search_similar_jobs  # ChromaDB functions for storing and searching JDs
from src.utils.helpers import load_job_descriptions          # Loads all .txt JD files from a folder into a dictionary


# Page Configuration
# Sets the browser tab title, icon, and layout width for the Streamlit app
st.set_page_config(page_title="ResumeScreening AI", page_icon="📄", layout="centered")

# Main heading shown at the top of the page
st.title("📄 ResumeScreening")

# Subtitle explaining what the app does
st.markdown("Upload your resume and get the top matching job roles ranked by skill match score.")
st.markdown("---")


# Load All Job Descriptions
# This loads all .txt files from the job_descriptions folder into a dictionary
# Key = filename (e.g. "DataScience.txt"), Value = full text of that JD
JD_FOLDER = "data/job_descriptions"
job_descriptions = load_job_descriptions(JD_FOLDER)

# If no JD files are found, stop the app and show an error message
if not job_descriptions:
    st.error("No job descriptions found in `data/job_descriptions/`. Please add .txt files there first.")
    st.stop()

# Index all JDs into ChromaDB so they are ready for vector similarity search
# This runs every time the app loads but skips JDs that are already stored
index_job_descriptions(job_descriptions)


# Sidebar — Admin JD Viewer
# The sidebar is on the left side and is meant for the admin/HR to view all open positions
with st.sidebar:
    # Section heading in the sidebar
    st.markdown("## 🏢 Open Positions")
    st.markdown("All active job descriptions loaded from the system.")
    st.markdown("---")

    # Build a clean list of JD names by removing the .txt extension for display
    jd_names = [name.replace(".txt", "") for name in job_descriptions.keys()]

    # Dropdown to select which JD to preview in the sidebar
    # This lets the admin/HR quickly read any JD without leaving the page
    selected_jd = st.selectbox("Select a JD to preview", options=jd_names)

    st.markdown("---")

    # Show the name of the selected JD as a heading
    st.markdown(f"### 📋 {selected_jd}")

    # Fetch the full text of the selected JD from the dictionary
    selected_jd_text = job_descriptions[selected_jd + ".txt"]

    # Display the full JD text in a read-only scrollable text area
    # disabled=True makes it read-only so the admin cant accidentally edit it
    # label_visibility="collapsed" hides the default label above the text area
    st.text_area("Job Description", value=selected_jd_text, height=400, disabled=True, label_visibility="collapsed")


# Resume Upload Input
# File uploader component — accepts multiple PDF files at once
# When files are uploaded, they are stored as a list of file-like objects in resume_files
resume_files = st.file_uploader(
    "📤 Upload Candidate Resume(s) (.pdf)",
    type=["pdf"],
    accept_multiple_files=True    # Allows uploading more than one resume at a time
)

# Slider to control how many top matching jobs to display after analysis
# ChromaDB always searches ALL JDs — this only controls how many results to show at the end
top_k = st.slider(
    "Number of top matches to show",
    min_value=1,
    max_value=len(job_descriptions),
    value=min(3, len(job_descriptions))
)

st.markdown("---")

# Analyze Button 
# When clicked, this triggers the full analysis pipeline below
# use_container_width=True makes the button stretch to full width
analyze = st.button("🔍 Find Matching Jobs", use_container_width=True)


# Main Analysis Pipeline
# This block only runs when the Analyze button is clicked
if analyze:

    # Show a warning if no resume was uploaded before clicking analyze
    if not resume_files:
        st.warning("Please upload at least one resume first.")

    else:
        # Loop through each uploaded resume one by one
        for resume_file in resume_files:

            # Show candidate name as a section header for each resume
            candidate_name = resume_file.name.replace(".pdf", "").replace("_", " ").title()
            st.markdown(f"---")
            st.markdown(f"## 👤 {candidate_name}")

            # Show a spinner while processing this specific resume
            with st.spinner(f"Analyzing {candidate_name}..."):

                # Save the uploaded PDF to a temporary file on disk
                # We need a real file path because pdf_parser reads from disk, not memory
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(resume_file.read())   # Write the uploaded file bytes to the temp file
                    tmp_path = tmp.name             # Save the temp file path for later use

                # Extract all text from the resume PDF using the temp file path
                resume_text = extract_text_from_pdf(tmp_path)

                # Delete the temp file immediately after extraction — we no longer need it
                os.unlink(tmp_path)

                # If the PDF had no readable text, skip this resume and move to the next
                if not resume_text.strip():
                    st.error(f"Could not extract text from {resume_file.name}. Skipping.")
                    continue

                # Send resume text to LLM to extract skills and experience as structured data
                resume_data = extract_document_data(resume_text)

                # Combine skills and experience into one summary list for LLM skill matching
                resume_summary = resume_data["skills"] + resume_data["experience"]

                # Convert resume text into a vector (embedding) for ChromaDB search
                resume_embedding = generate_embedding(resume_text)

                # Query ChromaDB for a wider candidate pool than what we display.
                # Always fetch at least 10 JDs (or all if fewer exist) so the LLM
                # has enough candidates to find the truly best skill matches.
                # The displayed results are trimmed to top_k AFTER LLM re-ranking.
                candidate_pool = max(10, top_k)
                candidate_pool = min(candidate_pool, len(job_descriptions))
                similar_jobs = search_similar_jobs(resume_embedding, top_k=candidate_pool)

                # For each matched JD, run LLM skill matching and calculate the ATS score
                job_results = []

                for job_id, job_text, distance in zip(
                    similar_jobs["ids"][0],        # List of matched JD filenames
                    similar_jobs["documents"][0],  # List of matched JD texts
                    similar_jobs["distances"][0]   # List of distances (lower = more similar)
                ):
                    # Extract required skills from this JD using LLM
                    jd_data = extract_document_data(job_text)
                    jd_skills = jd_data["skills"]

                    # Skip this JD if no skills could be extracted from it
                    if not jd_skills:
                        continue

                    # Use LLM to compare resume skills against JD skills intelligently
                    match_results = llm_skill_match(jd_skills, resume_summary)
                    matched = match_results["matched_skills"]
                    missing = match_results["missing_skills"]

                    # Calculate ATS score as a percentage of matched skills out of total JD skills
                    total = len(jd_skills)
                    matched_count = len(matched)
                    score = round((matched_count / total) * 100, 2) if total > 0 else 0

                    job_results.append({
                        "job": job_id.replace(".txt", ""),
                        "score": score,
                        "matched": matched,
                        "missing": missing,
                        "total": total,
                        "matched_count": matched_count
                    })

                # Sort all job results by score descending — best match first
                job_results.sort(key=lambda x: x["score"], reverse=True)

                # Trim to only show top_k results — LLM scored all JDs, now we limit display
                job_results = job_results[:top_k]

            # ── Results for this candidate ────────────────────────────────────
            st.markdown(f"### 🏆 Top Matching Jobs for {candidate_name}")

            if not job_results:
                st.info("No matching jobs found for this resume.")

            else:
                for rank, result in enumerate(job_results, start=1):
                    score = result["score"]

                    # Assign color and verdict based on score range
                    if score >= 80:
                        color = "🟢"
                        verdict = "Strong Match"
                    elif score >= 60:
                        color = "🔵"
                        verdict = "Good Match"
                    elif score >= 40:
                        color = "🟡"
                        verdict = "Partial Match"
                    else:
                        color = "🔴"
                        verdict = "Weak Match"

                    # Each job shown as a collapsible expander
                    with st.expander(f"{color} #{rank} — {result['job']}  |  {score}%  |  {verdict}"):

                        st.metric(
                            label="ATS Match Score",
                            value=f"{score}%",
                            delta=f"{result['matched_count']} of {result['total']} skills matched"
                        )
                        st.progress(int(score) / 100)
                        st.markdown("---")

                        col_a, col_b = st.columns(2)

                        with col_a:
                            st.markdown("**✅ Matched Skills**")
                            if result["matched"]:
                                for skill in result["matched"]:
                                    st.success(skill)
                            else:
                                st.info("No skills matched.")

                        with col_b:
                            st.markdown("**❌ Missing Skills**")
                            if result["missing"]:
                                for skill in result["missing"]:
                                    st.error(skill)
                            else:
                                st.info("No missing skills — perfect match!")
