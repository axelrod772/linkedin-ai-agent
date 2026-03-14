############################################
# Builder image: install Python dependencies
############################################
FROM python:3.11-slim AS builder

WORKDIR /app

# System dependencies for PyMuPDF and LinkedIn scraper
# Includes Chromium and Chrome driver so scraping works reliably in containers.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt


############################################
# Runtime image
############################################
FROM python:3.11-slim AS runtime

WORKDIR /app

# System dependencies required at runtime for scraping and PDF processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY linkedin_agent ./linkedin_agent
COPY main.py .

# Non-root user for security
RUN useradd -ms /bin/bash appuser
USER appuser

# Default environment variables (can be overridden at runtime)
ENV PYTHONUNBUFFERED=1 \
    LINKEDIN_DEFAULT_LOCATION=Remote \
    LINKEDIN_DEFAULT_NUM_JOBS=20

# The agent expects .env-style configuration; mount your own .env in production.

# Example command (override --resume with your own mounted resume path)
CMD ["python", "main.py", "--resume", "/app/resume.pdf", "--query", "AI Engineer", "--location", "Remote", "--top-k", "5"]

