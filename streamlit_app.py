"""
Streamlit GUI for CodeGuardian-AI
- Expects the analysis functions to be implemented in codeguardian.py:
    - analyze_code_text(code_text, language="python") -> dict
    - analyze_file(path) -> dict
    - analyze_repo(repo_url) -> dict (optional)
"""

import streamlit as st
from typing import Optional
import os

# Try to import the analysis functions from the codeguardian module.
try:
    from codeguardian import analyze_code_text, analyze_file, analyze_repo  # type: ignore
    CODEGUARDIAN_AVAILABLE = True
except Exception as e:
    CODEGUARDIAN_AVAILABLE = False
    _import_error = str(e)

st.set_page_config(page_title="CodeGuardian-AI GUI", layout="wide")

st.title("CodeGuardian-AI — GUI")
st.markdown(
    """
    A simple Streamlit app that wraps CodeGuardian-AI analysis functions.
    - Paste or upload code, or provide a GitHub URL, and get analysis results.
    """)

if not CODEGUARDIAN_AVAILABLE:
    st.warning(
        "codeguardian.py is not available or failed to import. Move/refactor notebook logic into codeguardian.py and install dependencies.\n\n"
        f"Import error: {_import_error}"
    )

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Input")
    input_mode = st.radio("Select input type", ["Paste code", "Upload file", "GitHub repo URL"])

    code_text: Optional[str] = None
    uploaded_file = None
    repo_url = ""

    if input_mode == "Paste code":
        code_text = st.text_area("Paste your code here", height=300, placeholder="# Paste your Python code")
    elif input_mode == "Upload file":
        uploaded_file = st.file_uploader("Upload a source code file", type=["py", "js", "ts", "java", "go", "txt"])
    else:
        repo_url = st.text_input("GitHub repo or file URL", "")

    st.markdown("### Settings")
    language = st.selectbox("Language (used for heuristics)", ["python", "javascript", "typescript", "java", "go", "other"])
    run_button = st.button("Run analysis")

with col2:
    st.header("Quick tips")
    st.markdown(
        """
        - For quick checks, paste a function or small file.
        - To analyze a repo, provide a GitHub URL (file or repo root).
        - Implement analyze_code_text / analyze_file / analyze_repo in codeguardian.py.
        """
    )
    st.markdown("### Output controls")
    st.checkbox("Show raw output", value=False, key="raw_output")

# Run analysis
if run_button:
    with st.spinner("Running analysis..."): 
        result = None
        try:
            if input_mode == "Paste code" and code_text:
                if CODEGUARDIAN_AVAILABLE:
                    result = analyze_code_text(code_text, language=language)
                else:
                    result = {"summary": "Placeholder (codeguardian missing)", "issues": [], "suggestions": []}
            elif input_mode == "Upload file" and uploaded_file:
                tmp_dir = "tmp_uploads"
                os.makedirs(tmp_dir, exist_ok=True)
                tmp_path = os.path.join(tmp_dir, uploaded_file.name)
                with open(tmp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                if CODEGUARDIAN_AVAILABLE:
                    result = analyze_file(tmp_path)
                else:
                    with open(tmp_path, "r", errors="ignore") as f:
                        content = f.read()
                    result = {"summary": "Placeholder (codeguardian missing)", "issues": [], "suggestions": [], "content": content}
            elif input_mode == "GitHub repo URL" and repo_url:
                if CODEGUARDIAN_AVAILABLE:
                    result = analyze_repo(repo_url)
                else:
                    result = {"summary": "Placeholder (codeguardian missing)", "issues": [], "suggestions": []}
            else:
                st.error("No input provided.")
        except Exception as e:
            st.exception(e)
            result = {"summary": f"Error running analysis: {e}", "issues": [], "suggestions": []}

    # Display results
    if result:
        st.header("Analysis result")
        st.subheader("Summary")
        st.write(result.get("summary", ""))

        st.subheader("Issues found")
        issues = result.get("issues", [])
        if issues:
            for i, issue in enumerate(issues, start=1):
                st.markdown(f"**{i}. {issue.get('title', 'Issue')}**")
                if issue.get("location"):
                    st.caption(f"Location: {issue['location']}\n")
                st.write(issue.get("description", ""))
                if issue.get("severity"):
                    st.markdown(f"- Severity: {issue['severity']}")
                st.markdown("---")
        else:
            st.info("No issues found (or the analysis module returned none).")

        st.subheader("Suggestions / Fixes")
        suggestions = result.get("suggestions", [])
        if suggestions:
            for s in suggestions:
                st.write("- " + s)
        else:
            st.info("No suggestions returned.")

        if st.session_state.get("raw_output"):
            st.subheader("Raw output")
            st.json(result)