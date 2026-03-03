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
            padding: 18mm 20mm;
            font-family: 'Calibri', 'Arial', sans-serif;
            font-size: 11pt;
            color: #1a1a1a;
            line-height: 1.5;
            border: 1px solid #dde1e7;
            box-shadow: 0 4px 24px rgba(0,0,0,0.09);
            box-sizing: border-box;
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

        /* ── Skills ── */
        .skills-text {
            color: #222;
            font-size: 11pt;
            line-height: 1.6;
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

        /* ── Contact bar ── */
        .contact-bar {
            text-align: center;
            font-size: 13px;
            color: #444;
            margin-top: 6px;
        }
        .contact-bar a {
            color: #1a3c6e;
            text-decoration: none;
            margin: 0 10px;
        }
        .contact-bar span { margin: 0 10px; color: #555; }

        /* ── Education & Project entries ── */
        .edu-entry, .proj-entry, .cert-entry { margin-bottom: 12px; }
        .edu-header, .proj-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }
        .edu-degree, .proj-name {
            font-weight: 700;
            font-size: 14px;
            color: #1a1a1a;
        }
        .edu-date, .proj-date {
            font-size: 13px;
            color: #555;
            white-space: nowrap;
        }
        .edu-school {
            font-style: italic;
            color: #444;
            font-size: 13.5px;
        }
        .proj-desc { color: #333; font-size: 13.5px; margin-top: 2px; }
        .cert-entry { color: #333; font-size: 13.5px; }
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
            "- GPA: 3.9/4.0"
        ),
        height=100,
    )

    projects = st.text_area(
        "🚀 Projects",
        placeholder=(
            "AI Chatbot (2023)\n"
            "- Built with Python & OpenAI API, 500+ active users\n\n"
            "E-Commerce Platform (2022)\n"
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
