"""Transparent keyword-based job-fit analysis.

The analyzer is intentionally deterministic: it does not call an LLM or infer
that a candidate has a skill merely because related words appear in a JD.
"""

import re
from typing import Dict, List

SKILL_TAXONOMY: Dict[str, Dict[str, List[str]]] = {
    "Excel": {"label": "Excel", "aliases": ["excel", "spreadsheet", "电子表格"]},
    "VLOOKUP": {"label": "VLOOKUP", "aliases": ["vlookup", "xlookup"]},
    "Pivot tables": {"label": "Pivot tables", "aliases": ["pivot table", "pivot tables", "数据透视表"]},
    "SQL": {"label": "SQL", "aliases": ["sql"]},
    "Python": {"label": "Python", "aliases": ["python"]},
    "Power BI": {"label": "Power BI", "aliases": ["power bi"]},
    "Tableau": {"label": "Tableau", "aliases": ["tableau"]},
    "Data analysis": {"label": "Data analysis", "aliases": ["data analysis", "data analytics", "数据分析"]},
    "Market research": {"label": "Market research", "aliases": ["market research", "市场调研"]},
    "User research": {"label": "User research", "aliases": ["user research", "用户调研", "用户研究"]},
    "Recruitment": {"label": "Recruitment", "aliases": ["recruitment", "talent acquisition", "招聘"]},
    "Sourcing": {"label": "Sourcing", "aliases": ["sourcing", "candidate sourcing", "人才寻访"]},
    "Onboarding": {"label": "Onboarding", "aliases": ["onboarding", "入职"]},
    "Learning and development": {"label": "Learning & Development", "aliases": ["learning and development", "l&d", "人才发展", "培训发展"]},
    "HRBP": {"label": "HRBP", "aliases": ["hrbp", "human resources business partner"]},
    "Performance management": {"label": "Performance management", "aliases": ["performance management", "绩效管理"]},
    "E-commerce operations": {"label": "E-commerce operations", "aliases": ["e-commerce operations", "ecommerce operations", "电商运营"]},
    "Product selection": {"label": "Product selection", "aliases": ["product selection", "选品"]},
    "GMV": {"label": "GMV", "aliases": ["gmv", "成交总额"]},
    "ROI": {"label": "ROI", "aliases": ["roi", "return on investment", "投资回报率"]},
    "Conversion rate": {"label": "Conversion rate", "aliases": ["conversion rate", "转化率"]},
    "Content operations": {"label": "Content operations", "aliases": ["content operations", "内容运营"]},
    "Xiaohongshu": {"label": "Xiaohongshu", "aliases": ["xiaohongshu", "小红书"]},
    "Douyin": {"label": "Douyin", "aliases": ["douyin", "抖音"]},
    "CapCut": {"label": "CapCut", "aliases": ["capcut", "剪映"]},
    "SEO": {"label": "SEO", "aliases": ["seo", "search engine optimization"]},
    "Campaign planning": {"label": "Campaign planning", "aliases": ["campaign planning", "活动策划", "营销活动"]},
    "Supply chain": {"label": "Supply chain", "aliases": ["supply chain", "供应链"]},
    "Inventory management": {"label": "Inventory management", "aliases": ["inventory management", "库存管理"]},
    "Pricing": {"label": "Pricing", "aliases": ["pricing", "定价"]},
    "Negotiation": {"label": "Negotiation", "aliases": ["negotiation", "谈判"]},
    "Project management": {"label": "Project management", "aliases": ["project management", "项目管理"]},
    "Communication": {"label": "Communication", "aliases": ["communication", "沟通能力"]},
    "English": {"label": "English", "aliases": ["english", "英语"]},
}


def _contains_alias(text: str, alias: str) -> bool:
    """Match English aliases as whole phrases and Chinese aliases literally."""
    source = text.casefold()
    term = alias.casefold()
    if re.search(r"[a-z0-9]", term):
        pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
        return re.search(pattern, source) is not None
    return term in source


def extract_skills(text: str) -> List[dict]:
    """Return taxonomy skills found in text, preserving taxonomy order."""
    found = []
    for key, item in SKILL_TAXONOMY.items():
        matched_aliases = [a for a in item["aliases"] if _contains_alias(text, a)]
        if matched_aliases:
            found.append({
                "key": key,
                "label": item["label"],
                "matched_aliases": matched_aliases,
            })
    return found


def analyze_job_fit(job_description: str, candidate_profile: str) -> dict:
    """Compare detected JD skills with profile evidence."""
    requirements = extract_skills(job_description)
    evidence = {item["key"]: item for item in extract_skills(candidate_profile)}
    matched = [item for item in requirements if item["key"] in evidence]
    gaps = [item for item in requirements if item["key"] not in evidence]
    total = len(requirements)
    ratio = (len(matched) / total * 100) if total else 0.0

    suggestions = []
    if gaps:
        suggestions.append(
            "Review each potential gap and add truthful evidence where you have relevant coursework, projects, or experience."
        )
    if matched:
        suggestions.append(
            "Strengthen matched skills with specific examples, tools used, scope, and measurable outcomes where available."
        )
    if not requirements:
        suggestions.append(
            "The JD did not match the current skill taxonomy. Review the wording or extend the taxonomy for this role."
        )
    suggestions.append(
        "Prioritize the requirements that appear most important in the JD; the current MVP treats all detected skills equally."
    )

    return {
        "requirements": requirements,
        "matched": matched,
        "gaps": gaps,
        "total_requirements": total,
        "match_ratio": ratio,
        "suggestions": suggestions,
    }


def build_llm_prompt(job_description: str, candidate_profile: str, result: dict) -> str:
    """Build a grounded prompt for optional review in a separate LLM."""
    matched = ", ".join(x["label"] for x in result["matched"]) or "None detected"
    gaps = ", ".join(x["label"] for x in result["gaps"]) or "None detected"
    return f"""Act as a careful career coach. Compare the job description with the candidate profile below.

Rules:
- Use only evidence explicitly present in the candidate profile.
- Do not invent employers, responsibilities, qualifications, dates, or performance metrics.
- Distinguish a missing keyword from a genuinely missing capability.
- Identify the 5 most important role requirements and explain the evidence for each.
- Suggest truthful, specific resume edits and 5 likely interview questions.
- If evidence is insufficient, say what information is missing.

A simple keyword scan detected these overlaps: {matched}
Potential keyword gaps (not proof of missing capability): {gaps}

JOB DESCRIPTION
---
{job_description}
---

CANDIDATE PROFILE
---
{candidate_profile}
---
"""


def build_markdown_report(result: dict, job_description: str, candidate_profile: str) -> str:
    """Create a portable Markdown summary without reproducing private contact data."""
    def bullet_items(items):
        return "\n".join(f"- {item['label']}" for item in items) or "- None detected"

    return f"""# Job Fit Analysis Report

## Summary
- Detected JD skills: {result['total_requirements']}
- Matched skills: {len(result['matched'])}
- Potential keyword gaps: {len(result['gaps'])}
- Keyword match ratio: {result['match_ratio']:.1f}%

## Matched skills
{bullet_items(result['matched'])}

## Potential gaps
{bullet_items(result['gaps'])}

## Suggested next steps
""" + "\n".join(f"- {item}" for item in result["suggestions"]) + """

## Interpretation
This report uses a fixed keyword taxonomy. A missing keyword is not proof that the candidate lacks a capability. The score is not a hiring probability or an objective measure of candidate quality. Review the original JD and profile before acting.
"""
