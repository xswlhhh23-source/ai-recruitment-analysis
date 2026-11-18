# Methodology and Responsible Use

## Purpose

This project helps a candidate understand a job description, compare it with their own written profile, and identify where clearer evidence may be needed. It is not an applicant tracking system and is not designed to rank or reject applicants.

## Current method

The MVP uses a manually maintained taxonomy of skills and aliases. For each taxonomy entry:

1. Search the job description for one or more aliases.
2. If an alias is found, include that skill in the detected JD requirements.
3. Search the candidate profile for the same skill aliases.
4. Mark the skill as matched if it appears in both texts; otherwise mark it as a potential keyword gap.

English phrases are matched case-insensitively with simple word boundaries. Chinese aliases are matched as literal substrings.

## Score

The keyword match ratio is:

`matched detected skills / all detected JD skills × 100`

All detected skills currently have equal weight. The ratio measures only coverage of the current taxonomy, not proficiency, relevance, experience depth, or interview performance.

## Known limitations

- Synonyms outside the taxonomy may be missed.
- A keyword may appear without meaningful evidence of competence.
- Skills can be demonstrated through transferable experience using different wording.
- The method does not understand context, seniority, recency, or the importance of each requirement.
- The taxonomy is not exhaustive and may need adjustment for different roles and industries.
- The generated LLM prompt is a separate optional workflow; this application does not call an LLM API.

## Responsible use

- Keep personal information out of pasted text unless it is essential.
- Do not use the score as a hiring decision or candidate ranking.
- Validate all output against the original resume and JD.
- Add only claims that the candidate can substantiate.
- Treat the tool as a reflection and preparation aid.
