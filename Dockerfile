FROM python:3.10

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port and run the server
EXPOSE 8000

CMD ["python", "whisper_fastapi_online_server.py", "--host", "0.0.0.0", "--port", "8000", "--warmup-file", "./jfk.wav"]

