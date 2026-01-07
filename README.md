# AI Resume Screening & Candidate Role Classifier

An intelligent Flask-based web application that screens resumes, extracts skills, and matches them against job descriptions with role classification.

## Features

- **Resume Parsing**: Extracts candidate name, email, phone, and 100+ technical skills
- **Skill Matching**: Compares resume skills against job description for match score (0-100%)
- **Role Classification**: Classifies candidates as Data Scientist, ML Engineer, or AI Engineer
- **Premium Dark UI**: Modern, responsive dashboard interface
- **Real-time Analysis**: Instant feedback on candidate fit

## Tech Stack

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, JavaScript
- **ML/NLP**: Regex-based skill extraction, skill taxonomy

## Installation

```bash
# Clone the repo
git clone https://github.com/melbin0610/ai-resume-screening.git
cd ai-resume-screening

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install flask

# Run the app
python app.py
