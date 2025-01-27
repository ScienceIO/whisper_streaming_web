FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port and run the server
EXPOSE 8000
CMD ["uvicorn", "whisper_fastapi_online_server:app", "--host", "0.0.0.0", "--port", "8000"]




