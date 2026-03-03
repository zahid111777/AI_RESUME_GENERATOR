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
    openai_api_key=OPENAI_API_KEY,
)

# ── Prompt template ──────────────────────────────────────────────────────────
RESUME_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an elite professional resume writer. "
                "Output ONLY a raw HTML snippet (no <html>, <head>, or <body> tags). "
                "Use this exact structure:\n\n"
                "<div class='resume'>\n"
                "  <div class='resume-header'>\n"
                "    <h1>{{Full Name}}</h1>\n"
                "  </div>\n"
                "  <div class='section'>\n"
                "    <div class='section-title'>Professional Summary</div>\n"
                "    <p>3-4 keyword-rich impactful sentences.</p>\n"
                "  </div>\n"
                "  <div class='section'>\n"
                "    <div class='section-title'>Core Competencies</div>\n"
                "    <div class='skills-grid'>\n"
                "      <span class='skill-tag'>Skill</span> ...\n"
                "    </div>\n"
                "  </div>\n"
                "  <div class='section'>\n"
                "    <div class='section-title'>Professional Experience</div>\n"
                "    <div class='job'>\n"
                "      <div class='job-header'><span class='job-title'>Title</span><span class='job-date'>Year–Year</span></div>\n"
                "      <div class='job-company'>Company Name</div>\n"
                "      <ul><li>Achievement bullet starting with action verb...</li></ul>\n"
                "    </div>\n"
                "  </div>\n"
                "</div>\n\n"
                "Rules:\n"
                "1. Output ONLY the HTML snippet — zero extra text, no markdown, no code fences.\n"
                "2. Every bullet must start with a strong action verb.\n"
                "3. Quantify achievements wherever possible (%, numbers, time saved).\n"
                "4. Do NOT invent facts — only elaborate naturally on what the user provides.\n"
                "5. Do NOT use tables."
            ),
        ),
        (
            "human",
            (
                "Create a professional resume for:\n\n"
                "Name: {name}\n\n"
                "Skills:\n{skills}\n\n"
                "Experience:\n{experience}\n\n"
                "Return only the HTML snippet."
            ),
        ),
    ]
)

# ── Public function called by the frontend ───────────────────────────────────
def generate_resume(name: str, skills: str, experience: str) -> str:
    """
    Generate a professional resume using LangChain + OpenAI.

    Parameters
    ----------
    name       : Full name of the candidate.
    skills     : Comma-separated or free-text list of skills.
    experience : Work experience description (free text).

    Returns
    -------
    A Markdown-formatted resume string.
    """
    chain = RESUME_PROMPT | llm
    response = chain.invoke(
        {"name": name, "skills": skills, "experience": experience}
    )
    return response.content
