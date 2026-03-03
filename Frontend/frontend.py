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
        .resume-box {
            background: #ffffff;
            border: 1px solid #d0d7de;
            border-radius: 10px;
            padding: 36px 40px;
            font-family: 'Georgia', serif;
            font-size: 15px;
            line-height: 1.75;
            color: #1a1a2e;
            box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        }
        .resume-box h1 {
            font-size: 2rem;
            text-align: center;
            color: #0d1b2a;
            margin-bottom: 4px;
        }
        .resume-box h2 {
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #1a6496;
            border-bottom: 2px solid #1a6496;
            padding-bottom: 4px;
            margin-top: 24px;
        }
        .resume-box ul { padding-left: 20px; }
        .resume-box li { margin-bottom: 4px; }
        .resume-box table { width: 100%; border-collapse: collapse; margin-top: 8px; }
        .resume-box td { padding: 4px 8px; }
        .resume-box hr { border: none; border-top: 1px solid #dee2e6; margin: 16px 0; }
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
                import markdown as md_lib
                try:
                    resume_html = md_lib.markdown(resume_md, extensions=["tables", "nl2br"])
                except Exception:
                    resume_html = resume_md.replace("\n", "<br>")
                st.markdown(
                    f'<div class="resume-box">{resume_html}</div>',

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
