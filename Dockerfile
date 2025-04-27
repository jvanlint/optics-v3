FROM python:3.12-slim-bullseye

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

# --- ADD THIS BLOCK ---
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    build-essential \
    git
&& rm -rf /var/lib/apt/lists/*
# -----------------------

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install other dependencies as needed