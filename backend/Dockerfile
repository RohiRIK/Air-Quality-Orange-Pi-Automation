# Use Python 3.11 Slim
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (required for some Python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    i2c-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
# Assuming build context is project root
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Expose port
EXPOSE 5000

# Run the application with Gunicorn
# -w 1: Single worker to ensure exclusive I2C access
# --threads 4: Handle concurrent requests
CMD ["gunicorn", "--workers=1", "--threads=4", "--bind=0.0.0.0:5000", "wsgi:app"]
