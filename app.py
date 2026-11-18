from datetime import datetime

import streamlit as st

from src.analyzer import analyze_job_fit, build_llm_prompt, build_markdown_report

st.set_page_config(
    page_title="AI Recruitment & Job Fit Analyzer",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 AI Recruitment & Job Fit Analyzer")
st.caption("An explainable assistant for understanding job requirements and preparing stronger, evidence-based applications.")

with st.expander("How this MVP works", expanded=False):
    st.write(
        "This version uses a transparent skill dictionary to compare a job description "
        "with a candidate profile. It does not send your text to an AI service. "
        "You can optionally copy the generated prompt into ChatGPT for a deeper qualitative review."
    )

left, right = st.columns(2)
with left:
    st.subheader("1. Job description")
    jd_text = st.text_area(
        "Paste the job description",
        height=320,
        placeholder="Paste the full job description here...",
        key="jd_text",
    )
with right:
    st.subheader("2. Candidate profile")
    profile_text = st.text_area(
        "Paste resume text or a concise profile",
        height=320,
        placeholder="Paste relevant education, experience, projects, skills and achievements here...",
        key="profile_text",
    )

analyze = st.button("Analyze job fit", type="primary", use_container_width=True)

if analyze:
    if not jd_text.strip() or not profile_text.strip():
        st.warning("Please provide both a job description and a candidate profile.")
    else:
        result = analyze_job_fit(jd_text, profile_text)
        st.session_state["analysis_result"] = result
        st.session_state["analysis_jd"] = jd_text
        st.session_state["analysis_profile"] = profile_text

if "analysis_result" in st.session_state:
    result = st.session_state["analysis_result"]
    jd = st.session_state["analysis_jd"]
    profile = st.session_state["analysis_profile"]

    st.divider()
    st.subheader("3. Analysis results")

    c1, c2, c3 = st.columns(3)
    c1.metric("Detected JD skills", result["total_requirements"])
    c2.metric("Matched skills", len(result["matched"]))
    c3.metric("Potential gaps", len(result["gaps"]))

    st.progress(result["match_ratio"] / 100 if result["total_requirements"] else 0)
    st.markdown(f"**Keyword match ratio: {result['match_ratio']:.1f}%**")
    st.caption("This is a keyword coverage indicator, not a hiring probability or an assessment of overall candidate quality.")

    tab1, tab2, tab3 = st.tabs(["Matched evidence", "Potential gaps", "Next steps"])
    with tab1:
        if result["matched"]:
            for item in result["matched"]:
                st.markdown(f"- **{item['label']}** — detected in both the JD and profile.")
        else:
            st.info("No taxonomy skills were detected in both texts. Consider checking wording or adding relevant evidence.")
    with tab2:
        if result["gaps"]:
            for item in result["gaps"]:
                st.markdown(f"- **{item['label']}** — appears in the JD but was not detected in the profile.")
            st.caption("A gap here may reflect different wording or missing resume evidence; it does not prove the candidate lacks the skill.")
        else:
            st.success("No potential gaps were detected by the current taxonomy.")
    with tab3:
        suggestions = result["suggestions"]
        for suggestion in suggestions:
            st.markdown(f"- {suggestion}")
        if not suggestions:
            st.write("Add more detail about responsibilities, tools, outcomes, and measurable evidence.")

    report = build_markdown_report(result, jd, profile)
    prompt = build_llm_prompt(jd, profile, result)

    st.subheader("4. AI-assisted qualitative review")
    st.write("Copy this prompt into ChatGPT or another LLM if you want a second-stage review. Check all outputs against the original evidence.")
    st.text_area("Generated prompt", prompt, height=230)
    st.download_button(
        "Download analysis report (.md)",
        data=report,
        file_name=f"job-fit-report-{datetime.now().strftime('%Y%m%d-%H%M')}.md",
        mime="text/markdown",
    )

st.divider()
st.caption("MVP 1.0 · Local analysis · No external API calls · Use as a preparation aid, not an automated hiring decision.")
