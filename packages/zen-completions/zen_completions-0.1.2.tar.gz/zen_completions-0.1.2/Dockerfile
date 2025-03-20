FROM python:3.10-slim

WORKDIR /app

# Copy all the source code first
COPY . .

# Install build deps, install package, then clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir . \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify installation and display version
RUN python -c "from zen_completions import __version__; print(f'zen-completions version: {__version__}')"

# Set environment variable to avoid Python writing bytecode files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENTRYPOINT ["zen"]
CMD ["--help"] 