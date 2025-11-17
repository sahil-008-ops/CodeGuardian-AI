# 🧠 AI Code Intelligence & Auto-Documentation System  
### *Next-Gen Developer Assistant Powered by Machine Learning + Static Analysis 🚀*

This project is a **full end-to-end AI engineering tool** that analyzes a codebase and automatically generates:

✔ Code Type Classification (ML-based)  
✔ Readability Quality Classification  
✔ Code Complexity Metrics (Cyclomatic Score + Nesting Depth)  
✔ Code Smell Detection (Security, Performance & Anti-patterns)  
✔ Smart Auto-Refactoring Suggestions  
✔ Auto-Generated Documentation (Markdown)

This system helps developers:  
🔹 Understand unfamiliar repos faster  
🔹 Improve security & readability  
🔹 Reduce debugging + maintenance effort  
🔹 Automate documentation work

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| **Function Classification** | ML-powered detection of function type (API/DB/Utility/ML/Data Processing) |
| **Readability Score** | Rates code from Low → Medium → High |
| **Complexity Analysis** | Cyclomatic complexity + logic depth detection |
| **Security Smells** | Detects SQL injection, `eval`, hardcoded secrets |
| **Performance Smells** | Over-nesting, long functions, too many parameters |
| **AI Refactoring Suggestions** | Adds docstrings, structure fixes, security notes |
| **Markdown Documentation Export** | Full intelligent report generated automatically |

---

## 🧩 Model Architecture

```
 ┌─────────────── Codebase (.py) ───────────────┐
 │                                               │
 │  1️⃣ AST Parser → Extract Functions + Metrics   │
 │  2️⃣ ML Classifier → Function Category          │
 │  3️⃣ Readability Classifier → Score Quality     │
 │  4️⃣ Code Smell Detection → Best Practices      │
 │  5️⃣ Auto-Refactor Suggestion Engine            │
 │  6️⃣ Markdown Report Generator (DOCUMENTATION)  │
 │                                               │
 └────────────────── Output 📄 ──────────────────┘
```

---

## 📁 Output Example

```
📌 sample_app.py — 5 functions analyzed

Function: UserRepository.get_user
Type: database
Readability: Low (score ≈ 4.2/10)
Complexity: 7  |  Depth: 6
Smells:
 - Deeply nested logic
 - SQL injection vulnerability
 - Hard-coded password

✨ Auto-Refactor Suggestions:
 - Add docstring
 - Use parameterized queries
```

➡ Full details stored in `DOCUMENTATION.md`

---

## 🔧 Installation & Usage (Colab Compatible)

### Clone Repo
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### Run in Google Colab
Upload:
- All `.py` files  
- The notebook `.ipynb` file  

Execute cells in order:  
✔ Train models  
✔ Upload code file  
✔ Generate documentation

### Analyze your own script

```python
file_path = "/content/your_script.py"
analyze_code_file(
    file_path,
    type_model=function_type_classifier,
    read_model=readability_classifier,
)
```

---

## 📦 Tech Stack

- Python 3.x  
- scikit-learn  
- AST (Abstract Syntax Tree) parsing  
- TF-IDF NLP features  
- Linear SVM classifiers  
- Markdown output generator

---

## 🔮 Future Enhancements

| Feature | Status |
|--------|:-----:|
| CodeBERT embeddings | 🚧 Planned |
| Unit Test Auto-Generation | 🚧 Planned |
| Web App (Streamlit / Gradio) | 🔜 Next |
| Support for JavaScript, Java, C++ | 🔜 Future |

---

## 👨‍💻 Author

**Sahil Kochar**  
MCA — Artificial Intelligence & Machine Learning  
Jain University  
📍 Bengaluru, India  

Portfolio: *(add your link here)*  
LinkedIn: *(add profile link)*  

---

## 🛡️ License

Open-source • Free to use • MIT License  

---

### ⭐ If this project helped you — Star the repo!

> Innovation isn’t magic — it’s automation. ⚡

