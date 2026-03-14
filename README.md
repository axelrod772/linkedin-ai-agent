## LinkedIn AI Agent – Resume & Job Match

This project is a production-oriented LinkedIn job scraping and resume-matching agent built for an **AI Engineer** portfolio. It turns a traditional notebook-style prototype into a modular LLM-powered agent with a CLI, a Streamlit UI, persistent memory, and Docker packaging.

The agent:

- **Scrapes LinkedIn job postings** for a given role and location.
- **Matches jobs against your resume** using a cosine-similarity baseline.
- **Generates targeted, LLM-powered suggestions** to improve your resume for the top matching jobs.
- **Persists memory** of previous profile–job interactions so future runs can reuse context.
- **Exposes both a CLI and Streamlit UI** so the same agent workflow can be driven from the terminal or a browser.

### Architecture Overview

The codebase is organized into a small Python package plus a CLI entrypoint:

- **`linkedin_agent/config.py`**: Loads configuration and secrets from environment / `.env`.
- **`linkedin_agent/tools.py`**: Scraping utilities, PDF parsing, and similarity scoring.
- **`linkedin_agent/memory.py`**: JSON-based persistent memory of profile–job interactions.
- **`linkedin_agent/agent.py`**: LangChain agent built with `create_openai_functions_agent`.
- **`main.py`**: Command-line entrypoint that wires everything together.

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
     +-----------------------+               |
                                             v
                                 +-----------+-----------+
                                 |  linkedin_memory.json |
                                 | (persistent memory)   |
                                 +-----------------------+
```

### Key Features

- **Modular architecture**: Clean separation of configuration, tools, memory, and agent orchestration.
- **LangChain-powered agent**: Uses `create_openai_functions_agent` with OpenAI models for tool-calling and stateful reasoning.
- **Context-aware messaging**: The agent reads prior suggestions for a profile and refines future guidance instead of starting from scratch.
- **Persistent JSON memory**: `linkedin_memory.json` stores historical profile–job interactions (title, company, score, suggestions).
- **Rate limiting protection**: LinkedIn scraping is executed with conservative settings and a small delay to avoid hammering the site; the number of analyzed jobs is configurable.
- **Containerized deployment**: Multi-stage `Dockerfile` produces a small runtime image for local or cloud deployment.

> **Note**: This project is intended for educational and personal portfolio use. When scraping LinkedIn or any other site, ensure that you comply with their terms of service.

> **Scraping vs. Sample Jobs**: In environments where LinkedIn changes its DOM or blocks automated access, the live scraper may return no results. When that happens, the agent automatically falls back to a small set of **curated, anonymized AI/ML job descriptions** modeled after real postings. This keeps the end‑to‑end scoring + LLM + memory pipeline demonstrable while being transparent that not all runs use live LinkedIn data.
>
> You can control this behavior with **`LINKEDIN_USE_SAMPLE_JOBS_IF_EMPTY`** (default: `true`) in your `.env`.

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

Make sure you have a resume in PDF format on disk, then run:

```bash
python main.py \
  --resume path/to/your_resume.pdf \
  --query "AI Engineer" \
  --location "Remote" \
  --top-k 5
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

The UI lets you upload a resume PDF, choose a target role and location, and browse the top-matching jobs and suggestions in expandable panels.

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

### How This Helps Your AI Engineer Resume

- **Demonstrates modern AI tooling**: Uses LangChain’s function-calling agents, a clear tools/memory/agent split, and both CLI and UI entrypoints that AI hiring managers will recognize.
- **Shows production-minded practices**: Environment-based configuration, persistent JSON memory, Docker, and a clean CLI interface suitable for automation.
- **Highlights responsible scraping**: Configurable limits and delays, a documented fallback to curated sample jobs, and clear separation of scraping concerns from LLM logic.

You can extend this further by:

- Evolving the web UI (e.g. richer filters, history views, and experiment toggles).
- Swapping in LangGraph for more advanced multi-step workflows.
- Integrating additional tools (Tavily, SerpAPI) to enrich job context before scoring.

