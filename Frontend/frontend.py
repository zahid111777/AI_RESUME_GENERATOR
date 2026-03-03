import sys
import os
from pathlib import Path

# Allow importing from Backend/
sys.path.append(str(Path(__file__).resolve().parent.parent / "Backend"))

import io
import traceback
import streamlit as st
import streamlit.components.v1 as components
from resume_export import build_pdf, build_docx
from app import generate_resume

# ── Font options ──────────────────────────────────────────────────────────────
FONT_MAP = {
    "🅜  Montserrat + Calibri  (Modern Bold — Default)": {
        "import_css": "@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&display=swap');",
        "heading": "'Montserrat', 'Candara', sans-serif",
        "body":    "'Calibri', 'Candara', 'Segoe UI', Arial, sans-serif",
    },
    "🅒  Calibri  (Corporate Classic)": {
        "import_css": "",
        "heading": "'Calibri', 'Segoe UI', sans-serif",
        "body":    "'Calibri', 'Segoe UI', Arial, sans-serif",
    },
    "🅒  Candara  (Stylish & Readable)": {
        "import_css": "",
        "heading": "'Candara', 'Segoe UI', sans-serif",
        "body":    "'Candara', 'Segoe UI', Arial, sans-serif",
    },
    "🅖  Georgia  (Traditional Serif)": {
        "import_css": "",
        "heading": "'Georgia', 'Times New Roman', serif",
        "body":    "'Georgia', serif",
    },
    "🅐  Arial  (Clean & Universal)": {
        "import_css": "",
        "heading": "Arial, 'Helvetica Neue', sans-serif",
        "body":    "Arial, 'Helvetica Neue', sans-serif",
    },
}

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
        /* ── MONTSERRAT FOR RESUME HEADING ── */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&display=swap');

        /* ── PAGE BACKGROUND — Gen-Z gradient ── */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
        }
        [data-testid="stHeader"] { background: transparent; }
        .block-container {
            padding-top: 2rem;
            max-width: 860px;
        }

        /* ── APP TITLE (Streamlit native title only) ── */
        [data-testid="stAppViewContainer"] > section > div > div > div > div h1 {
            background: linear-gradient(90deg, #a78bfa, #ec4899, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Inter', sans-serif !important;
            font-size: 2.4rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }

        /* ── FORM CARD — glassmorphism ── */
        [data-testid="stForm"] {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 20px;
            padding: 2rem;
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            box-shadow: 0 8px 40px rgba(0,0,0,0.4);
        }

        /* ── LABELS ── */
        label { color: #e2d9f3 !important; font-family: 'Inter', sans-serif !important; font-size: 0.88rem !important; font-weight: 500 !important; }

        /* ── INPUTS & TEXTAREAS ── */
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            background: #1a1a2e !important;
            border: 1px solid rgba(167,139,250,0.45) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            caret-color: #a78bfa !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.9rem !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border-color: #a78bfa !important;
            box-shadow: 0 0 0 3px rgba(167,139,250,0.25) !important;
        }
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder { color: #6b5fa0 !important; }

        /* ── SECTION HEADINGS inside form ── */
        [data-testid="stForm"] h5 {
            color: #a78bfa !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 0.3rem !important;
        }

        /* ── DIVIDER ── */
        hr { border-color: rgba(167,139,250,0.2) !important; }

        /* ── GENERATE BUTTON ── */
        [data-testid="stFormSubmitButton"] button {
            background: linear-gradient(90deg, #7c3aed, #db2777) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 12px !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            padding: 0.65rem 1.5rem !important;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 20px rgba(124,58,237,0.45) !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        }
        [data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 28px rgba(219,39,119,0.5) !important;
        }

        /* ── DOWNLOAD BUTTON ── */
        [data-testid="stDownloadButton"] button {
            background: linear-gradient(90deg, #0ea5e9, #6366f1) !important;
            color: #fff !important;
            border: none !important;
            border-radius: 12px !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 18px rgba(99,102,241,0.4) !important;
        }

        /* ── SUCCESS / ERROR banners ── */
        [data-testid="stAlert"] {
            border-radius: 12px !important;
            font-family: 'Inter', sans-serif !important;
        }
        /* success text visible on dark bg */
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        [data-testid="stAlert"] div {
            color: inherit !important;
        }

        /* ── SUBHEADER & headings outside form (visible on dark bg) ── */
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stHeadingWithActionElements"] h3,
        section[data-testid="stMain"] h3 {
            color: #e2d9f3 !important;
            font-family: 'Inter', sans-serif !important;
        }
        /* "Your AI-Generated Resume" subheader */
        .stMainBlockContainer h3 { color: #e2d9f3 !important; }

        /* ── STATUS WIDGET & SPINNER (visible on dark bg) ── */
        [data-testid="stStatusWidget"],
        [data-testid="stStatusWidget"] *,
        div[class*="StatusWidget"],
        div[class*="StatusWidget"] * {
            color: #f1f0ff !important;
        }
        [data-testid="stStatusWidget"],
        div[class*="StatusWidget"] {
            background: rgba(30,20,60,0.85) !important;
            border: 1px solid rgba(167,139,250,0.5) !important;
            border-radius: 14px !important;
            backdrop-filter: blur(10px) !important;
        }
        /* spinner text */
        [data-testid="stSpinner"] p,
        [data-testid="stSpinner"] span,
        [data-testid="stSpinner"] label {
            color: #c4b5fd !important;
            font-size: 0.95rem !important;
        }
        /* st.status() expander label */
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] p {
            color: #e2d9f3 !important;
        }
        [data-testid="stExpander"] {
            background: rgba(30,20,60,0.85) !important;
            border: 1px solid rgba(167,139,250,0.4) !important;
            border-radius: 14px !important;
        }

        /* ════════════════════════════════════════════
           PDF VIEWER WRAPPER
        ════════════════════════════════════════════ */
        .resume-viewer {
            background: #4a4e57;
            padding: 24px 0;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 18px;
        }

        /* ── Name header ── */
        .resume-header {
            text-align: center;
            margin-bottom: 14px;
        }
        .resume-header h1 {
            font-size: 22pt !important;
            font-weight: 800 !important;
            color: #1a3c6e !important;
            background: none !important;
            -webkit-background-clip: unset !important;
            -webkit-text-fill-color: #1a3c6e !important;
            margin: 0 !important;
            padding-bottom: 0 !important;
            border: none !important;
            border-bottom: none !important;
            letter-spacing: 2.5px !important;
            text-transform: uppercase !important;
            line-height: 1.15 !important;
            font-family: 'Montserrat', 'Candara', 'Calibri', sans-serif !important;
        }
        .resume-header .contact-bar {
            padding-bottom: 0;
            border-bottom: none;
            margin-bottom: 0;
        }

        /* prevent Streamlit color bleeding into resume-page */
        .resume-page p, .resume-page li,
        .resume-page div, .resume-page span { color: inherit; }

        /* ── Contact bar ── */
        .contact-bar {
            text-align: center;
            font-size: 9.5pt;
            color: #555;
            margin-top: 5px;
            letter-spacing: 0.3px;
        }
        .contact-bar a {
            color: #1a3c6e;
            text-decoration: none;
            margin: 0 8px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 9.5pt;
        }
        .contact-bar a:hover { text-decoration: underline; }
        /* force icon pseudo-elements to render inside resume-page */
        .resume-page .contact-bar .email-link::before,
        .resume-viewer .contact-bar .email-link::before {
            content: '' !important;
            display: inline-block !important;
            width: 13px !important; height: 13px !important;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%231a3c6e'%3E%3Cpath d='M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z'/%3E%3C/svg%3E") center/contain no-repeat !important;
            vertical-align: middle !important;
        }
        .resume-page .contact-bar .github-link::before,
        .resume-viewer .contact-bar .github-link::before {
            content: '' !important;
            display: inline-block !important;
            width: 13px !important; height: 13px !important;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%231a3c6e'%3E%3Cpath d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z'/%3E%3C/svg%3E") center/contain no-repeat !important;
            vertical-align: middle !important;
        }
        .resume-page .contact-bar .linkedin-link::before,
        .resume-viewer .contact-bar .linkedin-link::before {
            content: '' !important;
            display: inline-block !important;
            width: 13px !important; height: 13px !important;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%231a3c6e'%3E%3Cpath d='M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z'/%3E%3C/svg%3E") center/contain no-repeat !important;
            vertical-align: middle !important;
        }

        /* ── Sections ── */
        .section {
            margin-bottom: 11px;
        }
        .section-title {
            font-size: 8.5pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #1a3c6e;
            border-bottom: 1.5px solid #1a3c6e;
            padding-bottom: 2px;
            margin-bottom: 7px;
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
            line-height: 1.45;
        }

        /* ── Job entries ── */
        .job { margin-bottom: 9px; }
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
            margin-bottom: 3px;
            font-size: 10pt;
        }
        .job ul {
            margin: 3px 0 0 0;
            padding-left: 15px;
        }
        .job li {
            margin-bottom: 2px;
            color: #222;
            font-size: 10.5pt;
        }

        /* ── Education ── */
        .edu-entry { margin-bottom: 8px; }
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
            flex-shrink: 0;
            margin-left: 12px;
        }
        .edu-subheader {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-top: 1px;
        }
        .edu-school {
            font-style: italic;
            color: #3d3d3d;
            font-size: 10pt;
        }
        .edu-gpa {
            font-size: 9.5pt;
            color: #1a3c6e;
            font-weight: 600;
            white-space: nowrap;
            flex-shrink: 0;
            margin-left: 12px;
        }

        /* ── Projects ── */
        .proj-entry { margin-bottom: 8px; }
        .proj-entry:last-child { margin-bottom: 0; }
        .proj-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }
        .proj-name-group {
            display: inline-flex;
            align-items: baseline;
            gap: 8px;
        }
        .proj-name {
            font-weight: 700;
            font-size: 10.5pt;
            color: #111;
        }
        .proj-gh-link {
            font-size: 8.5pt;
            color: #1a3c6e;
            text-decoration: none;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 3px;
        }
        .proj-gh-link::before {
            content: '';
            display: inline-block;
            width: 10px; height: 10px;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%231a3c6e'%3E%3Cpath d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z'/%3E%3C/svg%3E") center/contain no-repeat;
            vertical-align: middle;
        }
        .proj-gh-link:hover { text-decoration: underline; }
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

        /* ── Certifications ── */
        .cert-entry {
            color: #2a2a2a;
            font-size: 10.5pt;
            margin-bottom: 4px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state init ────────────────────────────────────────────────────────
for _k in ("resume_html", "preview_html", "download_html", "pdf_bytes",
           "docx_bytes", "fn", "generated"):
    if _k not in st.session_state:
        st.session_state[_k] = None
if "generated" not in st.session_state:
    st.session_state.generated = False

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
    <div style='font-size:3rem; margin-bottom:0.3rem;'>✦</div>
    <h1 style='font-size:2.4rem; font-weight:800; background:linear-gradient(90deg,#a78bfa,#ec4899,#38bdf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent; margin:0;'>AI Resume Generator</h1>
    <p style='color:#c4b5fd; margin-top:0.5rem; font-size:1rem;'>Drop your details — get a pro resume in seconds ✨</p>
</div>
""", unsafe_allow_html=True)
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
            "CGPA: 3.9/4.0"
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

    st.markdown("---")
    st.markdown("##### 🎨 Resume Font")
    font_choice = st.selectbox(
        "Pick a font for your resume",
        options=list(FONT_MAP.keys()),
        index=0,
        label_visibility="collapsed",
        help="This affects the look of your downloaded resume",
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
        status = st.status("Generating your resume with AI ✨", expanded=True)
        status.write("📡 Sending your details to OpenAI...")
        with st.spinner("This may take 20–60 seconds for detailed inputs..."):
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

                # ── Apply selected font ───────────────────────────────
                _fnt         = FONT_MAP[font_choice]
                _fnt_import  = _fnt["import_css"]
                _fnt_heading = _fnt["heading"]
                _fnt_body    = _fnt["body"]

                # ── Shared screen CSS (flexbox OK here) ──────────────
                _screen_css = f"""
{_fnt_import}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #4a4e57; }}
.resume-viewer {{ background: #4a4e57; padding: 28px 0; display: flex; flex-direction: column; align-items: center; gap: 0; }}
.resume {{
    background: #ffffff;
    width: 210mm;
    padding: 15mm 18mm;
    font-family: {_fnt_body};
    font-size: 11pt;
    color: #1f1f1f;
    line-height: 1.45;
    box-shadow: 0 4px 24px rgba(0,0,0,0.45);
    box-sizing: border-box;
}}
.resume-header {{ text-align: center; margin-bottom: 14px; }}
.resume-header h1 {{ font-size: 22pt; font-weight: 800; color: #1a3c6e; letter-spacing: 2.5px; text-transform: uppercase; font-family: {_fnt_heading}; margin: 0; border: none; background: none; -webkit-text-fill-color: #1a3c6e; }}
.contact-bar {{ text-align: center; font-size: 9.5pt; color: #555; margin-top: 5px; }}
.contact-bar a {{ color: #1a3c6e; text-decoration: none; margin: 0 8px; }}
.section {{ margin-bottom: 11px; }}
.section-title {{ font-size: 8.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: #1a3c6e; border-bottom: 1.5px solid #1a3c6e; padding-bottom: 2px; margin-bottom: 7px; }}
.skills-text {{ font-size: 10.5pt; line-height: 1.45; color: #2a2a2a; }}
.section p {{ color: #2a2a2a; text-align: justify; margin: 0; }}
.job {{ margin-bottom: 9px; }}
.job-header {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1px; }}
.job-title {{ font-weight: 700; font-size: 10.5pt; color: #111; }}
.job-date {{ font-size: 9.5pt; color: #555; white-space: nowrap; }}
.job-company {{ font-style: italic; color: #3d3d3d; font-size: 10pt; margin-bottom: 3px; }}
.job ul {{ margin: 3px 0 0 0; padding-left: 15px; }}
.job li {{ margin-bottom: 2px; color: #222; font-size: 10.5pt; }}
.edu-entry {{ margin-bottom: 8px; }}
.edu-header {{ display: flex; justify-content: space-between; align-items: baseline; }}
.edu-degree {{ font-weight: 700; font-size: 10.5pt; color: #111; }}
.edu-date {{ font-size: 9.5pt; color: #555; white-space: nowrap; margin-left: 12px; }}
.edu-subheader {{ display: flex; justify-content: space-between; align-items: baseline; margin-top: 1px; }}
.edu-school {{ font-style: italic; color: #3d3d3d; font-size: 10pt; }}
.edu-gpa {{ font-size: 9.5pt; color: #1a3c6e; font-weight: 600; margin-left: 12px; }}
.proj-entry {{ margin-bottom: 8px; }}
.proj-header {{ display: flex; justify-content: space-between; align-items: baseline; }}
.proj-name-group {{ display: inline-flex; align-items: baseline; gap: 8px; }}
.proj-name {{ font-weight: 700; font-size: 10.5pt; color: #111; }}
.proj-gh-link {{ font-size: 8.5pt; color: #1a3c6e; text-decoration: none; font-weight: 500; }}
.proj-date {{ font-size: 9.5pt; color: #555; white-space: nowrap; }}
.proj-desc {{ color: #2a2a2a; font-size: 10.5pt; margin-top: 2px; }}
.cert-entry {{ font-size: 10.5pt; color: #2a2a2a; margin-bottom: 4px; }}
"""

                _fn = name.strip().replace(' ', '_')

                # Build preview HTML
                _preview_html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>{_screen_css}</style>
</head><body>
<div class="resume-viewer">
  {resume_html}
</div>
</body></html>"""

                # Build HTML download
                _download_html = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<title>{name.strip()} – Resume</title>
<style>
{_screen_css}
@media print {{
  body, html {{ background: none; }}
  .resume-viewer {{ background: none; padding: 0; }}
  .resume {{ box-shadow: none; width: 210mm; min-height: 297mm; }}
  @page {{ size: A4; margin: 0; }}
}}
</style></head>
<body><div class="resume-viewer">{resume_html}</div></body></html>"""

                # Build PDF bytes  (ReportLab — proper structured layout)
                try:
                    _pdf_bytes = build_pdf(resume_html, _fnt_heading, _fnt_body)
                except Exception:
                    _pdf_bytes = None

                # Build DOCX bytes  (python-docx — real styled paragraphs)
                try:
                    _docx_bytes = build_docx(resume_html, _fnt_heading, _fnt_body)
                except Exception:
                    _docx_bytes = None

                # ── Persist everything in session_state ───────────────
                st.session_state.generated     = True
                st.session_state.resume_html   = resume_html
                st.session_state.preview_html  = _preview_html
                st.session_state.download_html = _download_html
                st.session_state.pdf_bytes     = _pdf_bytes
                st.session_state.docx_bytes    = _docx_bytes
                st.session_state.fn            = _fn

                status.write("✅ Resume generated!")
                status.update(label="Done!", state="complete", expanded=False)
                st.success("✅ Resume generated! Scroll down to view and download.")

            except Exception as e:
                st.error(f"Error generating resume: {e}")
                st.code(traceback.format_exc(), language="python")

# ── Display & Downloads (persists across all re-runs / button clicks) ─────────
if st.session_state.generated:
    st.divider()
    st.subheader("Your AI-Generated Resume")
    components.html(st.session_state.preview_html, height=1350, scrolling=True)

    st.divider()
    st.markdown("##### ⬇️ Download Resume")
    _fn = st.session_state.fn

    dcol1, dcol2, dcol3 = st.columns(3)
    with dcol1:
        st.download_button(
            "🌐 HTML",
            data=st.session_state.download_html,
            file_name=f"{_fn}_resume.html",
            mime="text/html",
            use_container_width=True,
            key="dl_html",
            help="Open in browser → Ctrl+P → Save as PDF for best quality",
        )
    with dcol2:
        if st.session_state.pdf_bytes:
            st.download_button(
                "📄 PDF",
                data=st.session_state.pdf_bytes,
                file_name=f"{_fn}_resume.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="dl_pdf",
            )
        else:
            st.button("📄 PDF (unavailable)", disabled=True,
                      use_container_width=True, key="dl_pdf_na")
    with dcol3:
        if st.session_state.docx_bytes:
            st.download_button(
                "📝 Word (DOCX)",
                data=st.session_state.docx_bytes,
                file_name=f"{_fn}_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                key="dl_docx",
            )
        else:
            st.button("📝 DOCX (unavailable)", disabled=True,
                      use_container_width=True, key="dl_docx_na")
