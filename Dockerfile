FROM python:3.11-slim

# Install OS deps needed by pdfplumber (poppler, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpoppler-cpp-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

EXPOSE 5000

# Use gunicorn for production; bind to all interfaces
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "180"]
