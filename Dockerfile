FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure the directory exists at runtime
RUN mkdir -p /app/generated_audio

# Set environment variable for the storage directory
ENV AUDIO_DIR=/app/generated_audio

# Expose FastAPI port
EXPOSE 8000

# Command to run FastAPI app with Uvicorn
CMD ["uvicorn", "app.api.routes:app", "--host", "0.0.0.0", "--port", "8000"]
