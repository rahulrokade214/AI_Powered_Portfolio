import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Allow requests from your GitHub Pages site (and localhost for testing).
CORS(app, resources={r"/api/*": {"origins": [
    "https://rahulrokade214.github.io",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]}})

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=GROQ_API_KEY)

# System prompt: keeps the bot on-topic and answering as Rahul's portfolio assistant.
SYSTEM_PROMPT = """You are a helpful assistant embedded in Rahul Rokade's
portfolio website. Answer visitor questions about Rahul using the context
below. Be concise, friendly, and professional. If asked something outside
this context, politely say you can only answer questions about Rahul's
portfolio, and suggest they use the contact section to reach him directly.

About Rahul:
- # Rahul Sanjay Rokade — Profile Summary

## Contact & Online Presence
- **Email:** rahulrokade312@gmail.com
- **Phone:** +91 77960 72363
- **Portfolio:** https://rahulrokade214.github.io/Personal-Portfolio-Website-of-Rahul-Rokade/
- **GitHub:** https://github.com/rahulrokade214 (16 public repositories)
- **LinkedIn:** https://www.linkedin.com/in/rahul-rokade-a813b3286/
- **Location:** A/P-Puntamba, Taluka-Rahata, District-Ahmednagar, Maharashtra

## Professional Summary
Detail-oriented Data Analyst with hands-on experience in Power BI, SQL, Python, and Machine Learning. Skilled in building interactive dashboards, analyzing complex datasets, and generating actionable business insights, with a growing specialization in LLM-powered tools and agentic AI applications.

## Education
- **B.Tech, Electronics and Computer Engineering** — Sanjivani College of Engineering, Kopargaon (Dec 2021 – Jun 2025), CGPA 6.7
- **Coding Ninjas — Data Analytics Job Bootcamp** (In Progress, Jan 2026): Python, MySQL, Power BI, Excel, Statistics, BI concepts; hands-on dashboard building, EDA, predictive analytics, and KPI tracking

## Professional Experience
**Data Analytics Intern — ABB India Ltd, Nashik** (Apr–Jun 2025)
- Built a daily dynamic inventory management report in Power BI tracking inventory levels, order status, and item movement across the supply chain
- Created real-time visualizations, interactive dashboards, and automated alerts to reduce manual monitoring
- Built dynamic DAX measures and slicers for self-service, drill-down analytics by category/location/date
- Automated data refresh workflows, cutting report preparation time by 60%

## Technical Skills
- **Languages:** Python (Pandas, NumPy, Matplotlib, Seaborn), SQL (MySQL, ETL, query optimization)
- **BI & Analytics Tools:** Power BI (DAX, Power Query), Excel (pivot tables, VLOOKUP, macros), Tableau, Google Data Studio
- **LLMs & AI APIs:** Claude 3.5 Sonnet, GPT-4o/GPT-4 Turbo, LLaMA 3 (via Groq), Gemini 1.5 Pro — prompt engineering, structured JSON/CSV extraction, multi-turn conversation design
- **ML/AI:** Scikit-learn, TensorFlow, PyTorch, NLP, YOLO, regression/classification/clustering
- **Frameworks & Tools:** Django, Streamlit, FastAPI, Docker, Git/GitHub, Jupyter, VS Code, Google Colab

## Key Projects

### Claude AI Data Pipeline (Apr 2026)
[GitHub](https://github.com/rahulrokade214/Claude-AI-Data-Pipeline)

**What it does:** Automated Python pipeline pulling structured data from the Claude API using system+user prompt engineering, consolidating GitHub content via PyGithub, and auto-deploying outputs to GitHub via the REST API (no git CLI needed).

**Architecture (from stated tech stack):**
1. **Input layer** — natural language prompts sent to Claude (claude-sonnet), supplemented with local CSV/JSON seed files and GitHub repo content pulled via PyGithub's REST wrapper
2. **Prompt design** — system prompt constrains output to raw JSON/CSV only (no markdown fences/preamble); user prompt specifies exact schema, field names, and types
3. **Parsing & validation** — raw API text response parsed into structured Python objects
4. **Deployment layer** — script checks if a target file exists in the repo (`create_file` vs `update_file` via PyGithub), then commits directly through GitHub's REST API
5. **Modularity** — API interaction, parsing, file I/O, and GitHub upload are separated into independent functions for reuse across topics/output formats

**Suggested talking points (confirm/edit before using in interviews):**
- *Prompt reliability:* getting Claude to consistently return parse-ready JSON without hallucinated keys likely required iterating prompt wording — worth describing a before/after example if you recall one
- *Idempotency:* deciding when to create vs. update a file without git avoids duplicate commits — you can describe how you detected existing files
- *Error handling:* what happens if Claude's response isn't valid JSON — did you add retry logic or a fallback?

---

### Sales & Revenue Analytics Dashboard (Mar 2026)

**What it does:** End-to-end analytics solution: MySQL → Pandas → interactive Power BI dashboard. Applied RFM segmentation across 10,000+ customers (~15% campaign ROI improvement), built time-series forecasting at 92% accuracy, and automated weekly reporting (saving 5+ hrs/week).

**Architecture (from stated tech stack):**
1. **Data extraction** — raw sales/customer data queried from MySQL
2. **Transformation** — Pandas used to clean, join, and reshape data (likely handling nulls, duplicate customer records, and date normalization)
3. **Segmentation logic** — RFM (Recency, Frequency, Monetary) scoring computed per customer, then bucketed into segments (e.g. high-value, at-risk, churned)
4. **Forecasting** — time-series model built to project quarterly revenue (92% accuracy stated)
5. **Visualization layer** — Power BI dashboard surfacing revenue, regional performance, and segment breakdowns
6. **Automation** — Python scripts scheduled/run to regenerate weekly reports without manual re-pulling of data

**Suggested talking points (confirm/edit before using in interviews):**
- *Model choice:* which forecasting approach did you use (ARIMA, Prophet, linear regression on time features)? This affects how you'd explain the 92% accuracy figure
- *RFM thresholds:* how did you decide the cutoffs between segments — quartiles, business rules, or clustering?
- *Data quality:* MySQL sales data often has messy entries (returns, refunds, test orders) — worth mentioning if you had to filter these out

---

### AI Data Analyst Chatbot (Feb 2026)
[GitHub](https://github.com/rahulrokade214/Groq_AI_Chatbot)

**What it does:** Chatbot converting plain-English questions into SQL using LLaMA 3 via Groq, letting non-technical users query CSV/Excel data. Integrated Pandas + Plotly for instant visual insights (70% less manual reporting); deployed live on Streamlit Cloud with multi-turn memory.

**Architecture (from stated tech stack):**
1. **Frontend** — Streamlit UI for file upload (CSV/Excel) and chat interface
2. **NL-to-SQL layer** — user question + a schema description of the uploaded file sent to LLaMA 3 (via Groq API), which generates a SQL-like query or Pandas operation
3. **Execution layer** — generated query run against the in-memory dataframe (likely via `pandasql` or direct Pandas filtering, since there's no real DB)
4. **Visualization** — Plotly auto-generates charts based on the result shape
5. **Memory** — conversation history maintained across turns so follow-up questions ("now filter by region") retain context

**Suggested talking points (confirm/edit before using in interviews):**
- *SQL injection / safety:* since the LLM generates queries dynamically, how did you prevent it from generating destructive or malformed operations on the dataframe?
- *Schema awareness:* how does the model know column names/types from an arbitrary uploaded file — do you inject a schema summary into the prompt?
- *Chart selection logic:* how does the app decide which chart type (bar, line, pie) fits the result — a rule-based heuristic or another LLM call?

---

### DeskMate — Gesture & Voice Controlled AI Desktop Assistant (Nov 2025)

**What it does:** Real-time assistant combining YOLO object detection and NLP voice commands; analyzed usage logs with Pandas to improve command recognition accuracy by 20%.

**Architecture (from stated tech stack):**
1. **Vision layer** — YOLO model running on webcam feed via OpenCV to detect hand gestures/objects in real time
2. **Voice layer** — NLP-based voice command recognition running in parallel
3. **Command mapping** — recognized gesture/voice inputs mapped to desktop actions (e.g. open app, adjust volume)
4. **Feedback loop** — interaction logs captured and analyzed in Pandas to identify misrecognized commands, feeding back into accuracy improvements (20% gain stated)

**Suggested talking points (confirm/edit before using in interviews):**
- *Real-time performance:* running YOLO + voice recognition simultaneously is compute-heavy — did you optimize frame rate, use a lighter YOLO variant (nano/tiny), or run inference on a separate thread?
- *False positive handling:* how did you distinguish an intentional gesture from incidental hand movement in frame?
- *The 20% improvement:* what specifically changed after analyzing the logs — new gesture classes, retrained thresholds, or UI feedback to the user?



**Additional GitHub repositories:**
- [Ai-chatbot](https://github.com/rahulrokade214/Ai-chatbot) — Streamlit chatbot switchable between OpenAI and Ollama backends
- [ai-agents-for-beginners](https://github.com/rahulrokade214/ai-agents-for-beginners) — forked Microsoft learning repo on building AI agents
- Personal Portfolio Website — this profile's own site, deployed via GitHub Pages, with an integrated Groq-powered chatbot

## Certifications
- Data Visualization with Power BI — Coding Ninjas (2026)
- Data Analysis with Python — IBM (2026)
- Data Analytics Job Simulation — Deloitte (2026)

## Target Roles
Actively seeking opportunities in **Data Analytics**, **Agentic AI**, and **Generative AI/ML** roles.
"""



@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        message = (data.get("message") or "").strip()
        history = data.get("history") or []

        if not message:
            return jsonify({"error": "Empty message"}), 400

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        # Keep only the last 10 turns to control token usage.
        for turn in history[-10:]:
            role = turn.get("role")
            content = turn.get("content")
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": message})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.6,
            max_tokens=400,
        )
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("Chat error:", e)
        return jsonify({"error": "Something went wrong"}), 500


@app.route("/", methods=["GET"])
def serve_index():
    return send_from_directory('.', 'index.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
