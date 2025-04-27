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
    git \
    && rm -rf /var/lib/apt/lists/*
# -----------------------

COPY ../requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install other dependencies as needed

# Install Node.js and npm
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Verify installations
RUN node --version && npm --version

# Install Tailwind CSS globally
RUN npm install -g tailwindcss