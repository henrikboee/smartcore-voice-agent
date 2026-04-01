FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    pipecat-ai[google,deepgram,cartesia,daily,silero] \
    loguru

# Copy application code
COPY voice_agent.py .

# Expose port
EXPOSE 7860

# Run the voice agent
CMD ["python", "voice_agent.py"]
