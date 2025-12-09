# Use Python 3.9 Slim
FROM python:3.9-slim

# Set working directory
WORKDIR /app/backend

# Install system dependencies (required for some Python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    i2c-tools \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]