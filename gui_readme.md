# CodeGuardian-AI GUI

This folder adds a simple Streamlit-based GUI for CodeGuardian-AI.

Requirements
- Python 3.8+
- Install dependencies: `pip install -r requirements.txt`

How to run
1. Refactor the notebook logic: implement analyze_code_text / analyze_file in codeguardian.py by moving code from CodeGuardian_AI.ipynb.
2. Run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```
3. Open the browser UI (Streamlit will show a local URL).

Notes
- The provided codeguardian.py is a skeleton with simple heuristics. For production, move the notebook logic into it and adapt return values to the expected format.
- If you want, I can refactor the notebook into codeguardian.py and push these files in a branch and open a PR to the original repo.