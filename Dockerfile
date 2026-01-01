# Use Python 3.11 slim image for a smaller footprint
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# curl and healthcheck tools are good practice
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV HEADLESS_MODE=true
ENV API_PORT=8081

# Expose the port
EXPOSE 8081

# Create volume mount point ensures data dir exists
RUN mkdir -p /app/data

# Run the application
CMD ["python", "main.py"]
