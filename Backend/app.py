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
                "You are an elite professional resume writer with 15+ years of experience "
                "crafting ATS-optimized resumes for top-tier companies.\n\n"
                "Follow these rules strictly:\n"
                "1. Output ONLY clean Markdown — no commentary, no preamble.\n"
                "2. Use this exact structure (skip any section if data is missing):\n"
                "   - Centered name as H1\n"
                "   - A subtle divider line (---)\n"
                "   - ## Professional Summary  (3–4 punchy sentences, keyword-rich)\n"
                "   - ## Core Competencies    (skills in a 3-column pipe-separated table)\n"
                "   - ## Professional Experience (each role: bold title | Company | dates, then 3–5 bullet points)\n"
                "   - Closing horizontal rule (---)\n"
                "3. Each bullet point MUST start with a strong action verb.\n"
                "4. Quantify achievements wherever possible (%, $, users, time saved).\n"
                "5. Keep language concise, confident, and recruiter-friendly.\n"
                "6. Do NOT invent facts — only elaborate on what the user provides."
            ),
        ),
        (
            "human",
            (
                "Create a refined, professional resume for:\n\n"
                "Name: {name}\n\n"
                "Skills:\n{skills}\n\n"
                "Experience:\n{experience}\n\n"
                "Return only the Markdown resume."
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
