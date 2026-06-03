FROM python:3.11-slim-bullseye

WORKDIR /app

# System packages required by RDKit and Java-based chemistry tooling
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    libxrender1 \
    libxext6 \
    git \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (includes a git+ package, so git must be present)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and assets
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "💻_Home.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]
