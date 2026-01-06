import re
from dataclasses import dataclass
from typing import List, Dict, Literal

RoleType = Literal["data_scientist", "ml_engineer", "ai_engineer"]


@dataclass
class ParsedResume:
    name: str
    email: str
    phone: str
    skills: List[str]
    role_scores: Dict[RoleType, float]
    primary_role: RoleType | None
    raw_text: str


# ---- SKILL TAXONOMY FOR AI / DATA ROLES ----

CORE_SKILLS = {
    "programming": [
        "python", "r", "sql", "scala", "java", "c++",
        "bash", "pyspark",
    ],
    "ml_core": [
        "machine learning", "supervised learning", "unsupervised learning",
        "regression", "classification", "clustering", "recommendation systems",
        "feature engineering", "model evaluation", "cross validation",
        "hyperparameter tuning",
    ],
    "deep_learning": [
        "deep learning", "neural networks", "cnn", "rnn", "lstm",
        "transformers", "bert", "gpt", "computer vision",
        "nlp", "natural language processing",
    ],
    "frameworks": [
        "scikit-learn", "sklearn", "tensorflow", "pytorch",
        "keras", "xgboost", "lightgbm", "catboost",
    ],
    "data_engineering": [
        "data pipelines", "etl", "airflow", "spark", "hadoop",
        "kafka", "data warehouse", "snowflake", "bigquery",
    ],
    "statistics": [
        "statistics", "probability", "hypothesis testing",
        "a/b testing", "bayesian", "time series",
    ],
    "viz_bi": [
        "tableau", "power bi", "looker", "superset",
        "matplotlib", "seaborn", "plotly",
    ],
    "cloud_mle": [
        "aws", "azure", "gcp", "sagemaker", "vertex ai",
        "docker", "kubernetes", "mlops", "ci/cd",
    ],
}

ROLE_SKILLS: Dict[RoleType, List[str]] = {
    "data_scientist": (
        CORE_SKILLS["programming"]
        + CORE_SKILLS["ml_core"]
        + CORE_SKILLS["statistics"]
        + CORE_SKILLS["viz_bi"]
    ),
    "ml_engineer": (
        CORE_SKILLS["programming"]
        + CORE_SKILLS["ml_core"]
        + CORE_SKILLS["frameworks"]
        + CORE_SKILLS["cloud_mle"]
        + CORE_SKILLS["data_engineering"]
    ),
    "ai_engineer": (
        CORE_SKILLS["programming"]
        + CORE_SKILLS["deep_learning"]
        + CORE_SKILLS["frameworks"]
        + CORE_SKILLS["cloud_mle"]
    ),
}

ALL_SKILLS = sorted({s.lower() for skills in ROLE_SKILLS.values() for s in skills})


def extract_email(text: str) -> str:
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    m = re.search(pattern, text)
    return m.group(0) if m else "Not found"


def extract_phone(text: str) -> str:
    pattern = r"\+?\d[\d\s\-()]{7,}\d"
    m = re.search(pattern, text)
    return m.group(0) if m else "Not found"


def extract_name(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line[:80]
    return "Unknown"


def extract_skills(text: str) -> List[str]:
    low = text.lower()
    found: List[str] = []
    for skill in ALL_SKILLS:
        if skill in low:
            found.append(skill)
    return sorted(set(found))


def score_roles(skills: List[str]) -> Dict[RoleType, float]:
    skill_set = set(skills)
    scores: Dict[RoleType, float] = {}
    for role, role_skill_list in ROLE_SKILLS.items():
        rs = {s.lower() for s in role_skill_list}
        overlap = skill_set & rs
        scores[role] = round(len(overlap) / len(rs) * 100, 1) if rs else 0.0
    return scores


def choose_primary_role(role_scores: Dict[RoleType, float]) -> RoleType | None:
    if not role_scores:
        return None
    best_role, best_score = max(role_scores.items(), key=lambda kv: kv[1])
    return best_role if best_score >= 15.0 else None


def parse_resume(text: str) -> ParsedResume:
    text_clean = " ".join(text.split())
    skills = extract_skills(text_clean)
    role_scores = score_roles(skills)
    primary_role = choose_primary_role(role_scores)

    return ParsedResume(
        name=extract_name(text),
        email=extract_email(text_clean),
        phone=extract_phone(text_clean),
        skills=skills,
        role_scores=role_scores,
        primary_role=primary_role,
        raw_text=text_clean,
    )
