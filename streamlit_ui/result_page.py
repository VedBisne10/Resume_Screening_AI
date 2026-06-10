import streamlit as st   # Streamlit is used to render the UI components for the detail view


def show_result_detail(result):
    # This function displays the full detailed breakdown for a single candidate
    # It is called from dashboard.py inside an expander for each result row
    # result: a dictionary containing candidate name, score, matched/missing skills, education, job, status

    # Two column layout — left for score and skills, right for missing skills and education
    col1, col2 = st.columns(2)

    with col1:
        # Show the ATS score as a large metric
        st.metric(
            label="ATS Match Score",
            value=f"{result['score']}%"
        )

        # Show a progress bar representing the score visually
        st.progress(int(result["score"]) / 100)

        st.markdown("**✅ Matched Skills**")

        # Show each matched skill as a green tag
        if result["matched"]:
            matched_html = " ".join(
                f'<span style="background:#dcfce7; color:#166534; padding:3px 10px; border-radius:12px; font-size:13px; margin:2px; display:inline-block;">{s}</span>'
                for s in result["matched"]
            )
            st.markdown(matched_html, unsafe_allow_html=True)
        else:
            # If no skills matched, show a message
            st.caption("No skills matched.")

    with col2:
        st.markdown(f"**🏢 Job:** {result['job']}")
        st.markdown(f"**📊 Status:** {result['status']}")

        st.markdown("**❌ Missing Skills**")

        # Show each missing skill as a red tag
        if result["missing"]:
            missing_html = " ".join(
                f'<span style="background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:12px; font-size:13px; margin:2px; display:inline-block;">{s}</span>'
                for s in result["missing"]
            )
            st.markdown(missing_html, unsafe_allow_html=True)
        else:
            # If no skills are missing, the candidate is a perfect match
            st.caption("No missing skills — perfect match!")

        st.markdown("**🎓 Education**")

        # Show each education entry from the resume
        if result["education"]:
            for edu in result["education"]:
                # Education can be a dictionary with details or just a plain string
                if isinstance(edu, dict):
                    # If its a dictionary, extract degree, institute, and year
                    degree = edu.get("Degree", "")
                    institute = edu.get("Institute", "")
                    year = edu.get("Year", "")
                    st.caption(f"🏫 {degree} — {institute} ({year})")
                else:
                    # If its just a plain string, show it directly
                    st.caption(f"🏫 {edu}")
        else:
            st.caption("No education data found.")
