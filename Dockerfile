FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# System deps (minimal)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency spec first for better caching
COPY requirements.txt ./

# Install Python deps
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy app source
COPY . .

# Create data directories at runtime (if not mounted)
RUN mkdir -p data/raw data/processed

EXPOSE 8501

# The GROQ_API_KEY should be provided at runtime
ENV GROQ_API_KEY=""

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]


