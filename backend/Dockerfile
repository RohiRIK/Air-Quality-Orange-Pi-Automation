FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y     gcc     python3-dev     libgpiod-dev     python3-libgpiod     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get remove -y gcc python3-dev && apt-get autoremove -y

COPY bmp_reader.py .

ENV I2C_DEVICE /dev/i2c-0
ENV BLINKA_FORCEBOARD ORANGE_PI_3_LTS
ENV PYTHONUNBUFFERED=1

CMD ["python", "bmp_reader.py"]