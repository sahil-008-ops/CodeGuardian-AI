"""
Streamlit GUI for CodeGuardian-AI
Refactored per review:
- Use tempfile.TemporaryDirectory for uploads and ensure cleanup.
- Hide GitHub repo URL option until repo analysis implemented.
- Extract placeholder result helper to avoid duplication.
- Refactor analysis and rendering into run_analysis() and render_result().
- Use named expressions for simplified conditionals.
"""

import streamlit as st
from typing import Optional, Dict
import os
import tempfile

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
    A Streamlit app that wraps CodeGuardian-AI analysis functions.
    - Paste or upload code to get quick analysis, issues, and suggestions.

    Note: Repository analysis is currently disabled in the UI until a full
    implementation of analyze_repo is available.
    """
)

if not CODEGUARDIAN_AVAILABLE:
    st.warning(
        "codeguardian.py is not available or failed to import. Move/refactor notebook logic into codeguardian.py and install dependencies.\n\n"
        f"Import error: {_import_error}"
    )

# Shared placeholder result helper to avoid duplication
PLACEHOLDER_BASE = {"summary": "Placeholder (codeguardian missing)", "issues": [], "suggestions": []}

def placeholder_result(content: Optional[str] = None) -> Dict:
    r = PLACEHOLDER_BASE.copy()
    if content is not None:
        r["content"] = content
    return r


col1, col2 = st.columns([2, 1])

with col1:
    st.header("Input")
    # Hide GitHub repo URL option until implemented to avoid confusing users
    input_mode = st.radio("Select input type", ["Paste code", "Upload file"])

    code_text: Optional[str] = None
    uploaded_file = None

    if input_mode == "Paste code":
        code_text = st.text_area("Paste your code here", height=300, placeholder="# Paste your Python code")
    else:  # Upload file
        uploaded_file = st.file_uploader("Upload a source code file", type=["py", "js", "ts", "java", "go", "txt"])

    st.markdown("### Settings")
    language = st.selectbox("Language (used for heuristics)", ["python", "javascript", "typescript", "java", "go", "other"])
    run_button = st.button("Run analysis")

with col2:
    st.header("Quick tips")
    st.markdown(
        """
        - For quick checks, paste a function or small file.
        - Repository analysis is intentionally hidden until implemented.
        - Implement analyze_code_text / analyze_file / analyze_repo in codeguardian.py.
        """
    )
    st.markdown("### Output controls")
    st.checkbox("Show raw output", value=False, key="raw_output")


# Helper: centralize decision logic for running analysis

def run_analysis(input_mode: str, code_text: Optional[str], uploaded_file, language: str = "python") -> Dict:
    if input_mode == "Paste code":
        if not code_text:
            raise ValueError("No code provided for paste mode")
        return analyze_code_text(code_text, language) if CODEGUARDIAN_AVAILABLE else placeholder_result(code_text)

    if input_mode == "Upload file":
        if not uploaded_file:
            raise ValueError("No file uploaded")
        # Use a temporary directory to ensure cleanup
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = os.path.join(tmpdir, uploaded_file.name)
            # write bytes to disk
            with open(tmp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            if CODEGUARDIAN_AVAILABLE:
                # Let analyze_file handle file-related errors and return structured results
                return analyze_file(tmp_path)
            # If no analysis module, return placeholder including file content
            with open(tmp_path, "r", errors="ignore") as f:
                content = f.read()
            return placeholder_result(content)

    # Repo analysis is intentionally disabled in UI; keep a defensive branch
    raise ValueError(f"Unknown or unsupported input mode: {input_mode}")


# Helper: render the unified result

def render_result(result: Dict) -> None:
    st.header("Analysis result")
    st.subheader("Summary")
    st.write(result.get("summary", ""))

    st.subheader("Issues found")
    if (issues := result.get("issues", [])):
        for i, issue in enumerate(issues, start=1):
            st.markdown(f"**{i}. {issue.get('title', 'Issue')}**")
            if (loc := issue.get("location")):
                st.caption(f"Location: {loc}")
            st.write(issue.get("description", ""))
            if (sev := issue.get("severity")):
                st.markdown(f"- Severity: {sev}")
            st.markdown("---")
    else:
        st.info("No issues found (or the analysis module returned none).")

    st.subheader("Suggestions / Fixes")
    if (suggestions := result.get("suggestions", [])):
        for s in suggestions:
            st.write("- " + s)
    else:
        st.info("No suggestions returned.")

    if st.session_state.get("raw_output"):
        st.subheader("Raw output")
        st.json(result)


# Main trigger
if run_button:
    with st.spinner("Running analysis..."):
        try:
            result = run_analysis(input_mode, code_text, uploaded_file, language)
        except Exception as e:
            st.error(str(e))
            result = {"summary": f"Error: {e}", "issues": [], "suggestions": []}

    render_result(result)


# If repo analysis was requested previously, show a hint why it's disabled
st.caption("Repository analysis is disabled in the UI. To enable it, implement analyze_repo() in codeguardian.py and then re-enable the option.")
