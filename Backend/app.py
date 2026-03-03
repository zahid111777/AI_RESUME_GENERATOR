import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# ── Load API key from keys/.env ──────────────────────────────────────────────
env_path = Path(__file__).resolve().parent.parent / "keys" / ".env"
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found. Check keys/.env")

# ── LangChain model ──────────────────────────────────────────────────────────
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=OPENAI_API_KEY,    max_tokens=4096,
    request_timeout=120,)

# ── Prompt template ──────────────────────────────────────────────────────────
RESUME_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an elite professional resume writer. "
                "Output ONLY a raw HTML snippet (no <html>, <head>, or <body> tags). "
                "Use this exact structure — skip a section entirely if no data is provided for it:\n\n"
                "<div class='resume'>\n"
                "  <div class='resume-header'>\n"
                "    <h1>CANDIDATE NAME</h1>\n"
                "    <div class='contact-bar'>\n"
                "      <a class='email-link' href='mailto:email@example.com'>email@example.com</a>\n"
                "      <a class='github-link' href='https://github.com/username'>github.com/username</a>\n"
                "      <a class='linkedin-link' href='https://linkedin.com/in/username'>linkedin.com/in/username</a>\n"
                "    </div>\n"
                "  </div>\n"
                "  <div class='section'>\n"
                "    <div class='section-title'>Professional Summary</div>\n"
                "    <p>3-4 keyword-rich impactful sentences.</p>\n"
                "  </div>\n"
                "  <div class='section'>\n"
                "    <div class='section-title'>Core Competencies</div>\n"
                "    <div class='skills-text'>Python, JavaScript, React, ...</div>\n"
                "  </div>\n"
                "  <div class='section'>\n"
                "    <div class='section-title'>Professional Experience</div>\n"
                "    <div class='job'>\n"
                "      <div class='job-header'><span class='job-title'>Title</span><span class='job-date'>Year–Year</span></div>\n"
                "      <div class='job-company'>Company</div>\n"
                "      <ul><li>Achievement starting with action verb.</li></ul>\n"
                "    </div>\n"
                "  </div>\n"
                "  <div class='section'>\n"
                "    <div class='section-title'>Education</div>\n"
                "    <div class='edu-entry'>\n"
                "      <div class='edu-header'>\n"
                "        <span class='edu-degree'>Degree, Major</span>\n"
                "        <span class='edu-date'>Year–Year</span>\n"
                "      </div>\n"
                "      <div class='edu-subheader'>\n"
                "        <span class='edu-school'>University Name</span>\n"
                "        <span class='edu-gpa'>GPA: X.X</span>\n"
                "      </div>\n"
                "    </div>\n"
                "  </div>\n"
                "  <div class='section'>\n"
                "    <div class='section-title'>Projects</div>\n"
                "    <div class='proj-entry'>\n"
                "      <div class='proj-header'>\n"
                "        <div class='proj-name-group'>\n"
                "          <span class='proj-name'>Project Name</span>\n"
                "          <!-- if GitHub provided: --><a class='proj-gh-link' href='https://github.com/user/repo'>Project URL</a>\n"
                "        </div>\n"
                "        <span class='proj-date'>Year</span>\n"
                "      </div>\n"
                "      <div class='proj-desc'>Short impactful description.</div>\n"
                "    </div>\n"
                "  </div>\n"
                "  <div class='section'>\n"
                "    <div class='section-title'>Certifications</div>\n"
                "    <div class='cert-entry'>Certification Name – Issuer, Year</div>\n"
                "  </div>\n"
                "</div>\n\n"
                "Rules:\n"
                "1. Output ONLY the HTML snippet — no markdown, no code fences, no extra text.\n"
                "2. Every experience bullet must start with a strong action verb.\n"
                "3. Quantify achievements wherever possible.\n"
                "4. Do NOT invent facts — only elaborate on what the user provides.\n"
                "5. Do NOT use tables anywhere."
            ),
        ),
        (
            "human",
            (
                "Name: {name}\n"
                "Email: {email}\n"
                "GitHub: {github}\n"
                "LinkedIn: {linkedin}\n\n"
                "Skills:\n{skills}\n\n"
                "Experience:\n{experience}\n\n"
                "Education:\n{education}\n\n"
                "Projects:\n{projects}\n\n"
                "Certifications:\n{certifications}\n\n"
                "Return only the HTML snippet."
            ),
        ),
    ]
)

# ── Public function called by the frontend ───────────────────────────────────
def generate_resume(
    name: str,
    skills: str,
    experience: str,
    email: str = "",
    github: str = "",
    linkedin: str = "",
    education: str = "",
    projects: str = "",
    certifications: str = "",
) -> str:
    """Generate a professional HTML resume using LangChain + OpenAI."""
    chain = RESUME_PROMPT | llm
    response = chain.invoke(
        {
            "name": name,
            "email": email or "N/A",
            "github": github or "N/A",
            "linkedin": linkedin or "N/A",
            "skills": skills,
            "experience": experience,
            "education": education or "N/A",
            "projects": projects or "N/A",
            "certifications": certifications or "N/A",
        }
    )
    return response.content
