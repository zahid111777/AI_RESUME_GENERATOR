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

        /* ── Resume paper (A4) ── */
        .resume {
            background: #ffffff;
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            padding: 16mm 18mm 18mm 18mm;
            font-family: 'Calibri', 'Arial', sans-serif;
            font-size: 10.5pt;
            color: #1f1f1f;
            line-height: 1.55;
            border: 1px solid #d6dbe2;
            box-shadow: 0 6px 32px rgba(0,0,0,0.11);
            box-sizing: border-box;
        }

        /* ── Name header ── */
        .resume-header {
            text-align: center;
            padding-bottom: 12px;
            margin-bottom: 18px;
            border-bottom: 2.5px solid #1a3c6e;
        }
        .resume-header h1 {
            font-size: 26pt;
            font-weight: 700;
            color: #1a3c6e;
            margin: 0 0 6px 0;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            line-height: 1.1;
        }

        /* ── Contact bar ── */
        .contact-bar {
            text-align: center;
            font-size: 9.5pt;
            color: #555;
            margin-top: 4px;
            letter-spacing: 0.3px;
        }
        .contact-bar a {
            color: #1a3c6e;
            text-decoration: none;
        }
        .contact-bar a:hover { text-decoration: underline; }
        .contact-bar span { color: #555; }
        /* dot separator between contact items */
        .contact-bar > *:not(:last-child)::after {
            content: " ·";
            color: #999;
            margin: 0 6px 0 0;
        }

        /* ── Sections ── */
        .section {
            margin-bottom: 14px;
        }
        .section-title {
            font-size: 8.5pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2.2px;
            color: #1a3c6e;
            border-bottom: 1.5px solid #1a3c6e;
            padding-bottom: 3px;
            margin-bottom: 8px;
        }

        /* ── Summary ── */
        .section p {
            margin: 0;
            color: #2a2a2a;
            text-align: justify;
        }

        /* ── Skills ── */
        .skills-text {
            color: #2a2a2a;
            font-size: 10.5pt;
            line-height: 1.6;
        }

        /* ── Job entries ── */
        .job { margin-bottom: 12px; }
        .job:last-child { margin-bottom: 0; }
        .job-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 1px;
        }
        .job-title {
            font-weight: 700;
            font-size: 10.5pt;
            color: #111;
        }
        .job-date {
            font-size: 9.5pt;
            color: #555;
            white-space: nowrap;
            font-style: normal;
        }
        .job-company {
            font-style: italic;
            color: #3d3d3d;
            margin-bottom: 4px;
            font-size: 10pt;
        }
        .job ul {
            margin: 4px 0 0 0;
            padding-left: 16px;
        }
        .job li {
            margin-bottom: 3px;
            color: #222;
            font-size: 10.5pt;
        }

        /* ── Education ── */
        .edu-entry { margin-bottom: 10px; }
        .edu-entry:last-child { margin-bottom: 0; }
        .edu-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }
        .edu-degree {
            font-weight: 700;
            font-size: 10.5pt;
            color: #111;
        }
        .edu-date {
            font-size: 9.5pt;
            color: #555;
            white-space: nowrap;
        }
        .edu-school {
            font-style: italic;
            color: #3d3d3d;
            font-size: 10pt;
            margin-top: 1px;
        }
        .edu-gpa {
            font-size: 9.5pt;
            color: #555;
            margin-top: 2px;
        }

        /* ── Projects ── */
        .proj-entry { margin-bottom: 10px; }
        .proj-entry:last-child { margin-bottom: 0; }
        .proj-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }
        .proj-name {
            font-weight: 700;
            font-size: 10.5pt;
            color: #111;
        }
        .proj-date {
            font-size: 9.5pt;
            color: #555;
            white-space: nowrap;
        }
        .proj-desc {
            color: #2a2a2a;
            font-size: 10.5pt;
            margin-top: 2px;
        }
        .proj-link {
            font-size: 9.5pt;
            margin-top: 3px;
        }
        .proj-link a {
            color: #1a3c6e;
            text-decoration: none;
        }
        .proj-link a:hover { text-decoration: underline; }

        /* ── Certifications ── */
        .cert-entry {
            color: #2a2a2a;
            font-size: 10.5pt;
            margin-bottom: 4px;
            padding-left: 10px;
            border-left: 2px solid #1a3c6e;
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
    st.markdown("##### Personal Info")
    name = st.text_input("👤 Full Name", placeholder="e.g. John Doe")

    col1, col2, col3 = st.columns(3)
    with col1:
        email = st.text_input("📧 Email", placeholder="you@email.com")
    with col2:
        github = st.text_input("🐙 GitHub", placeholder="github.com/username")
    with col3:
        linkedin = st.text_input("💼 LinkedIn", placeholder="linkedin.com/in/username")

    st.markdown("---")
    st.markdown("##### Professional Details")

    skills = st.text_area(
        "🛠️ Skills",
        placeholder="e.g. Python, React, Node.js, Docker, AWS ...",
        height=100,
    )

    experience = st.text_area(
        "💼 Experience",
        placeholder=(
            "Software Engineer at Acme Corp (2021–2024)\n"
            "- Built REST APIs serving 1M+ requests/day\n\n"
            "Junior Developer at StartupXYZ (2019–2021)\n"
            "- Developed React dashboards ..."
        ),
        height=160,
    )

    education = st.text_area(
        "🎓 Education",
        placeholder=(
            "BSc Computer Science, MIT (2016–2020)\n"
            "GPA: 3.9/4.0"
        ),
        height=100,
    )

    projects = st.text_area(
        "🚀 Projects",
        placeholder=(
            "AI Chatbot (2023) | github.com/you/ai-chatbot\n"
            "- Built with Python & OpenAI API, 500+ active users\n\n"
            "E-Commerce Platform (2022) | github.com/you/ecommerce\n"
            "- Full-stack app with React & Node.js"
        ),
        height=120,
    )

    certifications = st.text_area(
        "📜 Certifications",
        placeholder=(
            "AWS Certified Solutions Architect – 2023\n"
            "Google Professional Data Engineer – 2022"
        ),
        height=80,
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
                resume_html = generate_resume(
                    name=name.strip(),
                    email=email.strip(),
                    github=github.strip(),
                    linkedin=linkedin.strip(),
                    skills=skills.strip(),
                    experience=experience.strip(),
                    education=education.strip(),
                    projects=projects.strip(),
                    certifications=certifications.strip(),
                )
                st.success("Resume generated successfully!")
                st.divider()

                # ── Display ──────────────────────────────────────────────
                st.subheader("Your AI-Generated Resume")
                st.markdown(resume_html, unsafe_allow_html=True)

                # ── Download ─────────────────────────────────────────────
                st.divider()
                st.download_button(
                    label="⬇️ Download Resume (.html)",
                    data=resume_html,
                    file_name=f"{name.strip().replace(' ', '_')}_resume.html",
                    mime="text/html",
                    use_container_width=True,
                )

            except Exception as e:
                st.error(f"Error generating resume: {e}")
