# 📄 ResumeScreening AI

An intelligent resume screening system that matches candidate resumes against job descriptions using a hybrid pipeline of vector similarity search and LLM-based skill evaluation.

## 🔗 Live Demo

> **Demo:** [Link coming soon](#)

---

## 🧠 How It Works

The system uses a two-stage pipeline to rank job matches:

1. **Vector Similarity (Stage 1)** — The resume is converted into an embedding vector using `sentence-transformers`. ChromaDB compares it against pre-indexed JD vectors and returns the top candidates by semantic similarity.

2. **LLM Skill Matching (Stage 2)** — The LLM evaluates each candidate JD against the resume's extracted skills and experience, returning a YES/NO verdict per skill. This produces an ATS score based on the percentage of matched skills.

3. **Final Ranking** — Results are sorted by ATS score (LLM) and the top-k are displayed — ensuring the best skill match wins, not just the best vector match.

---

## ✨ Features

- 📤 **Multi-resume upload** — analyze multiple candidate PDFs in one session
- 🔍 **Hybrid matching** — vector search narrows the pool, LLM ranks by actual skills
- 🧾 **Skill breakdown** — see exactly which skills matched and which are missing per job
- 📊 **ATS score** — percentage score showing how well the resume fits each JD
- 🏢 **JD viewer sidebar** — browse all open job descriptions directly in the UI
- 🎚️ **Adjustable top-k** — slider to control how many job matches to display
- 🟢🔵🟡🔴 **Match verdict** — color-coded rating (Strong / Good / Partial / Weak Match)
- 20 built-in job descriptions across roles including AI Engineer, Data Scientist, DevOps, Full Stack, Blockchain, and more

---

## 🗂️ Project Structure

```
ResumeScreeningAI/
│
├── streamlit_ui/
│   └── dashboard.py          # Main Streamlit web app
│
├── src/
│   ├── llm/
│   │   ├── llm_client.py     # OpenRouter API client
│   │   ├── extractor.py      # LLM-based skill/experience extractor
│   │   ├── skill_matcher.py  # LLM-based skill matching (YES/NO per skill)
│   │   └── prompts.py        # All prompt templates
│   │
│   ├── matcher/
│   │   ├── embedding_matcher.py  # Sentence-transformer embeddings
│   │   └── vector_store.py       # ChromaDB indexing and search
│   │
│   ├── parser/
│   │   ├── pdf_parser.py     # PDF text extraction
│   │   └── text_cleaner.py   # Text normalization for embeddings
│   │
│   └── utils/
│       └── helpers.py        # Job description file loader
│
├── data/
│   ├── job_descriptions/     # 20 JD text files
│   └── resumes/              # Sample resume PDFs
│
├── chroma_db/                # Persistent ChromaDB vector store
├── .streamlit/
│   └── secrets.toml          # API key (local dev only, not committed)
├── requirements.txt
└── app.py                    # CLI version of the pipeline
```

---

## ⚙️ Setup

### Prerequisites

- Python 3.10+
- An [OpenRouter](https://openrouter.ai) account (free tier works)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ResumeScreeningAI.git
cd ResumeScreeningAI
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenRouter API key

Create the file `.streamlit/secrets.toml` in the project root:

```toml
OPENROUTER_API_KEY = "sk-or-v1-your-key-here"
```

Get your free API key at [openrouter.ai/keys](https://openrouter.ai/keys).

### 5. Run the app

```bash
streamlit run streamlit_ui/dashboard.py
```

The app will open at `http://localhost:8501`.

---

## 🚀 Usage

1. Open the app in your browser
2. Upload one or more resume PDFs using the file uploader
3. Adjust the **top-k slider** to set how many job matches to show
4. Click **🔍 Find Matching Jobs**
5. View ranked results with matched/missing skills and ATS scores
6. Use the sidebar to preview any of the 20 available job descriptions

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| LLM | OpenRouter (`openai/gpt-oss-120b:free`) |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Vector DB | ChromaDB |
| PDF Parsing | PyPDF2 |
| Language | Python 3.10+ |

---

## 📋 Supported Job Roles

AI Engineer · Backend Developer · Blockchain Developer · Cloud Engineer (AWS) · Computer Vision Engineer · Cybersecurity Engineer · Data Engineer · Data Scientist · DevOps Engineer · Embedded Systems Engineer · Frontend Developer (React.js) · Full Stack Developer · GenAI Engineer · Java Developer · ML Engineer · Mobile App Developer (Flutter) · NLP Engineer · Python Developer · Site Reliability Engineer · SQL / Database Developer

(To add more JD's:
    1. Create a .txt file
    2. Paste the JD in the .txt file
    3. Move the .txt to data\job_descriptions
    4. Save)


---

## 📝 Notes

- The free tier of OpenRouter has rate limits. If you see rate limit errors, wait a moment and retry or reduce the top-k slider to 1–3.
- The app uses ChromaDB with persistent storage (`./chroma_db`). JD vectors are saved on first run and reused automatically.
- For Streamlit Cloud deployment, add `OPENROUTER_API_KEY` in your app's **Settings → Secrets**.
