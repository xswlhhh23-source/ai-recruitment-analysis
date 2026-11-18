# AI Recruitment & Job Fit Analyzer

An explainable, AI-assisted job application analysis tool. Paste a job description and a resume/profile to identify role requirements, compare evidence, find skill gaps, and prepare a structured prompt for deeper review with an LLM.

> **Current version: MVP 1.0** — a local Streamlit application with transparent, dictionary-based skill extraction. It does not call an external AI API and does not make hiring decisions.

## What it does

- Extracts role-related skills and requirements from a job description using a documented skill taxonomy.
- Detects skills evidenced in a candidate's resume/profile.
- Calculates a simple match ratio from the skills detected in the JD.
- Separates matched skills from potential gaps.
- Produces practical resume-improvement suggestions based on evidence already present in the profile.
- Generates a copy-ready prompt for ChatGPT or another LLM to conduct a more contextual review.
- Exports a Markdown report for record keeping.

## Run locally

Requires Python 3.10 or newer.

```bash
git clone https://github.com/xswlhhh23-source/ai-recruitment-analysis.git
cd ai-recruitment-analysis
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL printed by Streamlit (usually http://localhost:8501).

## How to use

1. Paste the complete job description.
2. Paste the resume text or a concise candidate profile.
3. Select **Analyze job fit**.
4. Review the detected requirements, evidence matches, and potential gaps.
5. Copy the generated LLM prompt for a second-stage qualitative review, or download the Markdown report.

A sample job description is available in [sample_data/job_description.txt](sample_data/job_description.txt).

## Method and scoring

The MVP uses a transparent skill taxonomy with English and Chinese aliases. A skill is counted as a JD requirement when one of its aliases appears in the JD text. A skill is counted as evidenced when one of its aliases appears in the candidate text.

**Match ratio = matched detected skills ÷ detected JD skills × 100%.**

This is a screening aid, not a probability of getting an interview or an objective measure of candidate quality. It does not assess context, proficiency, recency, depth of experience, or transferable skills. Review the evidence manually before making any decision.

See [docs/methodology.md](docs/methodology.md) for limitations and design choices.

## Project structure

```text
ai-recruitment-analysis/
├── app.py
├── src/
│   └── analyzer.py
├── tests/
│   └── test_analyzer.py
├── prompts/
│   └── jd_resume_analysis.md
├── sample_data/
│   └── job_description.txt
├── docs/
│   └── methodology.md
├── requirements.txt
└── README.md
```

## Responsible use

- Use only resumes and job descriptions you are authorized to process.
- Do not paste sensitive personal data such as ID numbers, home addresses, or private contact details.
- The tool is designed to support a candidate's preparation and reflection, not to rank or reject people.
- Do not treat missing keywords as proof that a person lacks a skill.
- Verify every suggested resume statement. Never add experience, metrics, or qualifications that are not true.

## Roadmap

- [x] Explainable JD-to-profile skill comparison
- [x] Evidence-based gap summary
- [x] LLM prompt generation
- [x] Markdown report export
- [x] Unit tests for core matching logic
- [ ] Editable skill taxonomy and role-specific weighting
- [ ] CSV batch analysis and comparison dashboard
- [ ] Optional LLM API integration with explicit user configuration

## Author

Personal portfolio project by **Xudong Sun**. Built to demonstrate practical use of AI-assisted workflows, recruitment analysis, structured problem solving, and Python application development.


## Deploy a public demo (Streamlit Community Cloud)

This repository is prepared for Streamlit Community Cloud. To publish the app:

1. Sign in at https://share.streamlit.io/ with GitHub.
2. Authorize access to your public repositories if prompted.
3. Select **Create app**.
4. Choose repository `xswlhhh23-source/ai-recruitment-analysis`, branch `main`, and entrypoint file `app.py`.
5. Choose an available app subdomain and click **Deploy**.

No API key or secret is required for MVP 1.0. The app runs the transparent local keyword-matching method and does not send resume text to an external model.

See the official [Streamlit deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Demo inputs

A fictional sample JD is provided in `sample_data/job_description.txt`. A fictional candidate profile is provided in `sample_data/candidate_profile.txt`. Both are illustrative test data, not a real person's resume or a real vacancy.
