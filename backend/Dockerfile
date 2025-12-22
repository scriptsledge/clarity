FROM python:3.10-slim-bookworm

WORKDIR /app

# Install runtime dependencies
# libgomp1 is often needed by torch for CPU parallelism
RUN apt-get update && apt-get install -y \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package installation
RUN pip install uv

# Copy requirements and install dependencies
COPY requirements.txt .
RUN uv pip install --no-cache-dir --system -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a non-root user (Hugging Face Spaces requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user
ENV PATH="/home/user/.local/bin:$PATH"

# Set environment variables
# HF Spaces uses port 7860 by default
EXPOSE 7860
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
