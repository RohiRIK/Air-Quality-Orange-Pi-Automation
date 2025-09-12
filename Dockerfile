# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install build dependencies and libgpiod
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libgpiod-dev \
    python3-libgpiod \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies to reduce image size (but keep libgpiod)
RUN apt-get remove -y gcc python3-dev && apt-get autoremove -y

# Copy the application files
COPY bmp_reader.py .
COPY app.py .
COPY dummy_sensor.py .
COPY templates/ templates/
COPY static/ static/

# Expose the port the app runs on
EXPOSE 5000

# Define environment variables
ENV I2C_DEVICE /dev/i2c-0
ENV BLINKA_FORCEBOARD ORANGE_PI_3_LTS
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["python", "app.py"]
