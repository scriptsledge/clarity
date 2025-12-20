# Stage 1: Builder
FROM python:3.10-slim-bookworm AS builder
WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Configure uv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy requirements
COPY requirements.txt .

# Create venv and install dependencies
# We allow building from source for llama-cpp-python to ensure libc compatibility
RUN uv venv /app/.venv && \
    uv pip install \
    --no-cache \
    -r requirements.txt \
    --python /app/.venv

# Stage 2: Final Runtime Image
FROM python:3.10-slim-bookworm
WORKDIR /app

# Install runtime dependencies (OpenMP support for llama.cpp)
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user

EXPOSE 7860
ENV MODEL_CTX_SIZE=8192

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]