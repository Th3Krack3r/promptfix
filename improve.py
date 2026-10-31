"""Rule-based prompt improvement. No AI API calls, no dependencies.

Takes a vague prompt and restructures it into Role / Task / Context /
Constraints / Output format sections, and produces two variants:
a concise one and a detailed one.
"""

import re

# (keywords, role) -- checked in order, first match wins.
ROLE_RULES = [
    (["code", "coding", "debug", "bug", "python", "javascript", "program",
      "function", "error", "crash", "script", "sql", "api"],
     "expert software developer"),
    (["resume", "cv", "cover letter", "job", "interview", "career",
      "hiring", "linkedin"],
     "experienced career coach"),
    (["essay", "homework", "school", "study", "exam", "thesis",
      "assignment", "teacher", "student"],
     "patient tutor"),
    (["marketing", "ad", "advertisement", "social media", "brand",
      "audience", "sales copy", "seo"],
     "marketing strategist"),
    (["business", "startup", "plan", "revenue", "pricing", "investor",
      "pitch"],
     "business advisor"),
    (["workout", "fitness", "diet", "weight", "muscle", "nutrition",
      "exercise"],
     "fitness and nutrition coach"),
    (["legal", "contract", "law", "lawyer", "lease", "lawsuit"],
     "legal information assistant (not a lawyer, for general "
     "information only)"),
    (["recipe", "cook", "meal", "baking", "dinner"],
     "experienced home chef"),
    (["travel", "trip", "itinerary", "vacation", "flight", "hotel"],
     "travel planner"),
    (["health", "symptom", "doctor", "illness", "medical"],
     "health information assistant (not a doctor, for general "
     "information only)"),
]

FORMAT_RULES = [
    (["code", "debug", "bug", "error", "crash", "fix my"],
     "working code in a code block, followed by a short explanation of "
     "what was wrong and what changed"),
    (["list", "ideas", "options", "ways to"],
     "a numbered list, each item with a one-line explanation"),
    (["compare", "versus", "vs", "difference between", "pros and cons"],
     "a comparison with clear headings, then a short recommendation"),
    (["essay", "write about", "write something"],
     "a structured piece with an introduction, clear sections, and a "
     "conclusion"),
    (["explain", "what is", "how does", "why"],
     "a clear explanation with headings and a concrete example"),
    (["plan", "schedule", "routine", "itinerary"],
     "a step-by-step plan with headings for each part"),
    (["resume", "cv", "cover letter"],
     "a polished, ready-to-use draft"),
]

GENERIC_QUESTIONS = [
    "What outcome do you want? (e.g. a decision, a draft, an explanation)",
    "Who is this for, and what background do they already have?",
    "Any constraints? (length, tone, format, deadline, things to avoid)",
]


def _words(text):
    return re.findall(r"[A-Za-z0-9']+", text)


def _match(rules, text):
    lowered = text.lower()
    for keywords, value in rules:
        if any(k in lowered for k in keywords):
            return value
    return None


def _article(role):
    return "an" if role[:1].lower() in "aeiou" else "a"


def _clean_task(text):
    """Turn the raw input into a single task sentence."""
    t = " ".join(text.split())
    # Strip common filler openers so the task reads cleanly.
    t = re.sub(r"^(please\s+|can you\s+|could you\s+|i need\s+|i want\s+"
               r"|help me\s+|help\s+)", "", t, flags=re.IGNORECASE)
    t = t.strip().rstrip(".")
    if not t:
        return t
    return t[0].upper() + t[1:]


def improve(prompt):
    """Return a dict with concise/detailed variants and metadata."""
    raw = prompt.strip()
    word_count = len(_words(raw))
    task = _clean_task(raw)
    role = _match(ROLE_RULES, raw) or "helpful expert"
    output_format = _match(FORMAT_RULES, raw) or (
        "a structured answer with headings and a short summary at the end")

    constraints = [
        "Be specific and concrete; avoid generic filler.",
        "If anything is ambiguous, state your assumption before answering.",
    ]
    if word_count < 15:
        constraints.append(
            "Ask up to 3 clarifying questions first if the request is "
            "still unclear, then answer with your best assumptions.")

    concise = (
        f"Act as {_article(role)} {role}. {task}. "
        f"Be specific and concrete, avoid generic filler, and state any "
        f"assumptions if the request is ambiguous. "
        f"Format the answer as {output_format}."
    )

    lines = [
        f"Role: Act as {_article(role)} {role}.",
        "",
        f"Task: {task}.",
        "",
        "Context: (Add 1-2 sentences here about your situation, audience, "
        "or goal -- the more specific, the better the answer.)",
        "",
        "Constraints:",
    ]
    lines += [f"- {c}" for c in constraints]
    lines += [
        "",
        f"Output format: {output_format}.",
    ]
    detailed = "\n".join(lines)

    result = {
        "role": role,
        "word_count": word_count,
        "concise": concise,
        "detailed": detailed,
        "note": None,
        "questions": [],
    }
    if word_count < 15:
        result["note"] = (
            "Your prompt is very short, so the improved versions above "
            "are best guesses. Answering these will sharpen it a lot:")
        result["questions"] = GENERIC_QUESTIONS
    return result
