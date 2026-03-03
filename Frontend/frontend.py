import sys
import os
from pathlib import Path

# Allow importing from Backend/
sys.path.append(str(Path(__file__).resolve().parent.parent / "Backend"))

import streamlit as st
from app import generate_resume

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Generator",
    page_icon="📄",
    layout="centered",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        .block-container { padding-top: 2rem; }
        .stTextArea textarea { font-size: 14px; }

        /* ── Resume paper ── */
        .resume {
            background: #ffffff;
            max-width: 860px;
            margin: 0 auto;
            padding: 48px 56px;
            font-family: 'Calibri', 'Arial', sans-serif;
            font-size: 14px;
            color: #1a1a1a;
            line-height: 1.6;
            border: 1px solid #dde1e7;
            border-radius: 4px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.09);
        }

        /* ── Name header ── */
        .resume-header {
            text-align: center;
            border-bottom: 3px solid #1a3c6e;
            padding-bottom: 14px;
            margin-bottom: 22px;
        }
        .resume-header h1 {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1a3c6e;
            margin: 0 0 4px 0;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        /* ── Section titles ── */
        .section { margin-bottom: 20px; }
        .section-title {
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #1a3c6e;
            border-bottom: 1.5px solid #1a3c6e;
            padding-bottom: 3px;
            margin-bottom: 10px;
        }

        /* ── Summary ── */
        .section p {
            margin: 0;
            color: #333;
        }

        /* ── Skills grid ── */
        .skills-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .skill-tag {
            background: #eef2f8;
            color: #1a3c6e;
            border: 1px solid #c5d0e0;
            border-radius: 4px;
            padding: 3px 10px;
            font-size: 13px;
            font-weight: 500;
        }

        /* ── Job entries ── */
        .job { margin-bottom: 16px; }
        .job-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }
        .job-title {
            font-weight: 700;
            font-size: 14.5px;
            color: #1a1a1a;
        }
        .job-date {
            font-size: 13px;
            color: #555;
            white-space: nowrap;
        }
        .job-company {
            font-style: italic;
            color: #444;
            margin-bottom: 6px;
            font-size: 13.5px;
        }
        .job ul {
            margin: 4px 0 0 0;
            padding-left: 18px;
        }
        .job li {
            margin-bottom: 4px;
            color: #222;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ───────────────────────────────────────────────────────────────────
st.title("📄 AI Resume Generator")
st.markdown("Paste your details below and let AI craft a professional resume for you.")
st.divider()

# ── Input form ───────────────────────────────────────────────────────────────
with st.form("resume_form"):
    name = st.text_input(
        "👤 Full Name",
        placeholder="e.g. John Doe",
    )

    skills = st.text_area(
        "🛠️ Skills",
        placeholder=(
            "e.g. Python, Machine Learning, Data Analysis, "
            "Communication, Project Management ..."
        ),
        height=120,
    )

    experience = st.text_area(
        "💼 Experience",
        placeholder=(
            "e.g.\n"
            "Software Engineer at Acme Corp (2021–2024)\n"
            "- Built REST APIs serving 1M+ requests/day\n"
            "- Led a team of 4 engineers\n\n"
            "Junior Developer at StartupXYZ (2019–2021)\n"
            "- Developed React dashboards ..."
        ),
        height=200,
    )

    submitted = st.form_submit_button("✨ Generate Resume", use_container_width=True)

# ── Generation ───────────────────────────────────────────────────────────────
if submitted:
    if not name.strip():
        st.error("Please enter your full name.")
    elif not skills.strip():
        st.error("Please enter at least one skill.")
    elif not experience.strip():
        st.error("Please describe your experience.")
    else:
        with st.spinner("Generating your resume with AI..."):
            try:
                resume_md = generate_resume(
                    name=name.strip(),
                    skills=skills.strip(),
                    experience=experience.strip(),
                )
                st.success("Resume generated successfully!")
                st.divider()

                # ── Display ──────────────────────────────────────────────
                st.subheader("Your AI-Generated Resume")
                st.markdown(resume_md, unsafe_allow_html=True)

                # ── Download ─────────────────────────────────────────────
                st.divider()
                st.download_button(
                    label="⬇️ Download Resume (.md)",
                    data=resume_md,
                    file_name=f"{name.strip().replace(' ', '_')}_resume.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

            except Exception as e:
                st.error(f"Error generating resume: {e}")
