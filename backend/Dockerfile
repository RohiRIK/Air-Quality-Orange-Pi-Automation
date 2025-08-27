FROM python:3.9-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc python3-dev libgpiod-dev python3-libgpiod && rm -rf /var/lib/apt/lists/*

RUN pip uninstall -y adafruit-blinka adafruit-platformdetect && \
    pip install --no-cache-dir --upgrade adafruit-blinka adafruit-platformdetect
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["tail", "-f", "/dev/null"]
