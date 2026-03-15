## LinkedIn AI Agent – Resume & Job Match

This project is a production-oriented LinkedIn job scraping and resume-matching agent built for an **AI Engineer** portfolio. It turns a traditional notebook-style prototype into a modular LLM-powered agent with a CLI, a Streamlit UI, a FastAPI service, persistent memory (JSON + ChromaDB), and Docker packaging.

The agent:

- **Scrapes LinkedIn job postings** for a given role and location.
- **Matches jobs against your resume** using a cosine-similarity baseline.
- **Generates targeted, LLM-powered suggestions** to improve your resume for the top matching jobs.
- **Persists memory** of previous profile–job interactions so future runs can reuse context.
- **Stores semantic job/profile embeddings** in a local **ChromaDB** vector store for similarity-based recall.
- **Exposes both a CLI, a Streamlit UI, and a FastAPI API** so the same agent workflow can be driven from the terminal, a browser, or HTTP.

### Architecture Overview

The codebase is organized into a small Python package plus multiple entrypoints:

- **`linkedin_agent/config.py`**: Loads configuration and secrets from environment / `.env`.
- **`linkedin_agent/tools.py`**: Scraping utilities, PDF parsing, and similarity scoring.
- **`linkedin_agent/memory.py`**: JSON-based persistent memory of profile–job interactions.
- **`linkedin_agent/vector_memory.py`**: ChromaDB-based semantic memory for profiles and jobs.
- **`linkedin_agent/query_intent.py`**: Natural-language search intent parser (`SearchIntent`, `parse_search_intent`).
- **`linkedin_agent/agent.py`**: LangChain agent built with `create_openai_functions_agent` plus a structured outreach planner.
- **`linkedin_agent/sample_jobs_data.py`**: Curated sample job postings used when live scraping returns no results.
- **`main.py`**: Command-line entrypoint that wires everything together.
- **`ui_app.py`**: Streamlit UI for running the workflow in a browser.
- **`api.py`**: FastAPI app exposing the outreach planner as an HTTP API.

#### Text-Based Architecture Diagram

```text
                 +---------------------------+
                 |        CLI / main.py      |
                 |  (parse args, orchestrate)|
                 +-------------+-------------+
                               |
                               v
                 +-------------+-------------+
                 |     linkedin_agent        |
                 |                           |
     +-----------+-----------+   +-----------+-----------+
     |       config.py       |   |        agent.py       |
     |  - load_settings()    |   |  - build LC agent     |
     +-----------+-----------+   |  - run_workflow()     |
                 |               +-----------+-----------+
                 |                           |
                 v                           v
     +-----------+-----------+   +-----------+-----------+
     |       tools.py        |   |      memory.py        |
     | - scrape_linkedin_jobs()  |  | - JSONMemoryStore  |
     | - extract_text_from_pdf() |  | - InteractionRecord|
     | - resume_job_desc_match() |  +-----------+--------+
     +-----------+-----------+               |
                 |                           v
                 v               +-----------+-----------+
     +-----------+-----------+   |  vector_memory.py     |
     |   api.py / ui_app.py  |   | - ChromaDB store      |
     | - FastAPI / Streamlit |   | - profile similarity  |
     +-----------------------+   +-----------+-----------+
                                             |
                                             v
                                 +-----------+-----------+
                                 |  linkedin_memory.json |
                                 |  chroma_db/           |
                                 | (persistent memory)   |
                                 +-----------------------+
```

### Key Features

- **Modular architecture**: Clean separation of configuration, tools, memory, agent orchestration, and API layer.
- **LangChain-powered agent**: Uses `create_openai_functions_agent` with OpenAI models for tool-calling and stateful reasoning.
- **Structured outreach planning**: A Pydantic `OutreachPlan` model and output parser ensure every outreach message includes `subject`, `message`, `strategy`, `tone`, and `industry`.
- **Context-aware messaging**: The agent reads prior suggestions for a profile and refines future guidance instead of starting from scratch.
- **Persistent JSON + vector memory**: `linkedin_memory.json` stores historical profile–job interactions while `chroma_db/` stores semantic embeddings for similarity search.
- **Centralized logging**: All agent “thoughts” and “actions” are logged to `logs/agent.log` via a rotating file handler.
- **Rate limiting protection**: LinkedIn scraping is executed with conservative settings and a small delay to avoid hammering the site; the number of analyzed jobs is configurable.
- **Containerized deployment**: Multi-stage `Dockerfile` produces a small runtime image for local or cloud deployment, including Chromium and the Chrome driver for scraping.

> **Note**: This project is intended for educational and personal portfolio use. When scraping LinkedIn or any other site, ensure that you comply with their terms of service.

> **Scraping vs. Sample Jobs**: In environments where LinkedIn changes its DOM or blocks automated access, the live scraper may return no results. When that happens, the agent automatically falls back to **curated sample jobs** from `linkedin_agent/sample_jobs_data.py` (diverse roles and locations so any resume can get a match). This keeps the end‑to‑end scoring + LLM + memory pipeline demonstrable while being transparent that not all runs use live LinkedIn data.
>
> You can control this behavior with **`LINKEDIN_USE_SAMPLE_JOBS_IF_EMPTY`** (default: `true`) in your `.env`.

#### Authenticated scraping (recommended)

The scraper library supports an **authenticated session** so LinkedIn treats the run as a logged-in user. That usually returns more jobs and fewer timeouts than anonymous mode.

1. **Get your `li_at` cookie**
   - Log in to [linkedin.com](https://www.linkedin.com) in Chrome (or Edge).
   - Open DevTools (F12) → **Application** (or **Storage**) → **Cookies** → `https://www.linkedin.com`.
   - Find the cookie named **`li_at`** and copy its **Value** (long string).
2. **Put it in `.env`**
   - Add a line: `LI_AT_COOKIE=paste_the_value_here` (no quotes).
   - Do not commit `.env` or share this value; it is a session secret.
3. **Run the app**
   - The scraper reads `LI_AT_COOKIE` from the environment. If it is set, it uses the authenticated strategy instead of the deprecated anonymous one.

The `li_at` cookie can expire (often after a short time or when you log out). If scraping starts failing again, refresh the cookie from the browser and update `.env`.

### Setup Instructions

#### 1. Clone the Project

```bash
git clone https://github.com/axelrod772/linkedin-ai-agent.git
cd linkedin-ai-agent
```

#### 2. Create and Populate `.env`

Copy the example environment file and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env` and set at least:

- **`OPENAI_API_KEY`**: Your OpenAI API key.
- **`OPENAI_MODEL_NAME`**: e.g. `gpt-4o-mini` or another chat model that supports tool-calling.

Optional:

- **`NVIDIA_API_KEY`**, **`NVIDIA_MODEL_NAME`** if you want to experiment with NVIDIA endpoints separately.
- **`LINKEDIN_DEFAULT_LOCATION`**, **`LINKEDIN_DEFAULT_NUM_JOBS`**, **`LINKEDIN_MEMORY_PATH`** to tune defaults.
- **`LINKEDIN_CHROMA_DIR`**: Directory where the ChromaDB vector store will persist (default: `chroma_db`).
- **`LINKEDIN_MAX_JOB_AGE_DAYS`**, **`LINKEDIN_DEFAULT_EXPERIENCE_LEVEL`**, **`LINKEDIN_PAGE_TIMEOUT_SECONDS`**, **`AGENT_DEFAULT_TOP_K`**: Scraper and agent defaults (see `.env.example`).
- **`LI_AT_COOKIE`**: For authenticated LinkedIn scraping (see “Authenticated scraping” above).

#### 3. Install Dependencies (Local Dev)

Using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

> The key libraries are `langchain`, `langchain-openai`, `linkedin-jobs-scraper`, `pymupdf`, and `scikit-learn`.

#### 4. Run the Agent Locally (CLI)

Make sure you have a resume in PDF format on disk. You can use either a structured query or a **natural-language** description:

**Structured query:**

```bash
python main.py \
  --resume path/to/your_resume.pdf \
  --query "AI Engineer" \
  --location "Remote" \
  --top-k 5
```

**Natural-language query** (the agent parses role, location, experience, and time window):

```bash
python main.py \
  --resume path/to/your_resume.pdf \
  --natural-query "look for AI engineer roles with no experience in Hyderabad posted in the last 24 hours"
```

You should see output similar to:

- Top matching jobs (title, company, location, score).
- A link to each job.
- Concrete bullet-point suggestions for improving your resume for each job.

Optionally, you can emit results as structured JSON:

```bash
python main.py \
  --resume path/to/your_resume.pdf \
  --query "Machine Learning Engineer" \
  --output-json results.json
```

#### 5. Run the Streamlit UI

If you prefer a browser-based workflow, you can use the Streamlit app defined in `ui_app.py`:

```bash
streamlit run ui_app.py
```

The UI lets you upload a resume PDF, then either enter a **target role and location** or describe your search in **plain language** (e.g. “Look for AI engineer roles with no experience in Hyderabad posted in the last 24 hours”). You can also set “Only include jobs from last N days” and use the **Outreach planner demo** (paste a LinkedIn profile summary and get a structured outreach plan). Results appear as expandable panels with job links and improvement suggestions.

#### 6. Run the FastAPI Outreach API

To demonstrate the outreach planner as a service, run the FastAPI app with Uvicorn:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Then send a LinkedIn-style profile summary via `POST`:

```bash
curl -X POST http://localhost:8000/api/linkedin-messenger \
  -H "Content-Type: application/json" \
  -d '{
    "profile_summary": "Senior ML engineer at a fintech startup working on fraud detection and credit risk models..."
  }'
```

The API responds with a structured JSON outreach plan:

```json
{
  "subject": "...",
  "message": "...",
  "strategy": "...",
  "tone": "professional",
  "industry": "Fintech"
}
```

### Docker Usage

#### 1. Build the Image

```bash
docker build -t linkedin-ai-agent .
```

#### 2. Run the Container

Mount your resume and `.env` file into the container:

```bash
docker run --rm \
  -v $(pwd)/.env:/app/.env \
  -v /absolute/path/to/your_resume.pdf:/app/resume.pdf \
  linkedin-ai-agent \
  python main.py --resume /app/resume.pdf --query "AI Engineer" --location "Remote" --top-k 5
```

On **Windows PowerShell**, use `${PWD}` for the current directory:

```bash
docker run --rm `
  -v ${PWD}\.env:/app/.env `
  -v C:\absolute\path\to\your_resume.pdf:/app/resume.pdf `
  linkedin-ai-agent `
  python main.py --resume /app/resume.pdf --query "AI Engineer" --location "Remote" --top-k 5
```

You can also rely on the `CMD` defined in the `Dockerfile` and only override the resume path with environment variables or a different command as needed.

### Tests

From the project root:

```bash
pytest
```

Runs unit tests for job-age parsing and the JSON memory store (see `tests/test_utils.py`).

### How This Helps Your AI Engineer Resume

- **Demonstrates modern AI tooling**: Uses LangChain’s function-calling agents, a clear tools/memory/agent split, and both CLI and UI entrypoints that AI hiring managers will recognize.
- **Shows production-minded practices**: Environment-based configuration, persistent JSON memory, Docker, and a clean CLI interface suitable for automation.
- **Highlights responsible scraping**: Configurable limits and delays, a documented fallback to curated sample jobs, and clear separation of scraping concerns from LLM logic.

You can extend this further by:

- Evolving the web UI (e.g. richer filters, history views, and experiment toggles).
- Swapping in LangGraph for more advanced multi-step workflows.
- Integrating additional tools (Tavily, SerpAPI) to enrich job context before scoring.

