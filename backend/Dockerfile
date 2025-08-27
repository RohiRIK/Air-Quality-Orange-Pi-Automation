FROM python:3.9-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade adafruit-blinka adafruit-platformdetect

COPY . .

CMD bash -c "env; python app.py"