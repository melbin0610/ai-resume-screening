from __future__ import annotations

import os
from flask import Flask, render_template, request, jsonify
from backend.resume_parser import parse_resume


# -------------------------------------------------
# Flask app setup (templates in frontend/templates)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "frontend", "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)


# ----------------- ROUTES ------------------------

@app.route("/", methods=["GET"])
def home():
    """
    Render the main UI page.
    """
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Accepts:
      - job_description (text, from form)
      - resume_text    (text, from form)

    Returns JSON with:
      - candidate_name
      - email, phone
      - skills           (all detected skills)
      - matched_skills   (skills also present in job description)
      - match_score      (0–100, based on skill overlap)
      - role_scores      (per‑role coverage: data_scientist / ml_engineer / ai_engineer)
      - primary_role     (best‑fit role or null)
    """
    job_desc = request.form.get("job_description", "") or ""
    resume_text = request.form.get("resume_text", "") or ""

    if not job_desc.strip() or not resume_text.strip():
        return jsonify({"error": "Please provide both job description and resume text."}), 400

    # --- Parse resume (name, contact, skills, role scores) ---
    parsed = parse_resume(resume_text)

    # --- Simple skill match vs JD ---
    jd_lower = job_desc.lower()
    matched_skills = [s for s in parsed.skills if s in jd_lower]

    if parsed.skills:
        match_score = round(len(matched_skills) / len(parsed.skills) * 100, 1)
    else:
        match_score = 0.0

    response = {
        "candidate_name": parsed.name,
        "email": parsed.email,
        "phone": parsed.phone,
        "skills": parsed.skills,
        "matched_skills": matched_skills,
        "match_score": match_score,
        "role_scores": parsed.role_scores,
        "primary_role": parsed.primary_role,
    }

    return jsonify(response)


# -------------- ENTRY POINT ----------------------

if __name__ == "__main__":
    # For local development. In production, run via Gunicorn/Uvicorn, etc.
    app.run(host="0.0.0.0", port=5000, debug=True)
