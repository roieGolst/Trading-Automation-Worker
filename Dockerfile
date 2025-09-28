FROM ubuntu:22.04

# Environment variables
ENV WORKER_PYTHON_VERSION=3.9
ENV CLI_TOOL_PYTHON_VERSION=3.12

ENV PYENV_ROOT=/root/.pyenv
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    curl \
    git \
    ca-certificates \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    xz-utils \
    libffi-dev \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Install pyenv & Python 3.9 + 3.12
RUN curl https://pyenv.run | bash \
    && pyenv update \
    && pyenv install "$WORKER_PYTHON_VERSION" \
    && pyenv install "$CLI_TOOL_PYTHON_VERSION" \
    && pyenv global "$WORKER_PYTHON_VERSION" "$CLI_TOOL_PYTHON_VERSION" \
    && pyenv rehash

# Set the working directory
WORKDIR /app

# Copy requirements & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files
COPY . .

# Make & run your build scripts with bash
RUN chmod +x ./scripts/build_auto_rsa.sh ./scripts/proto_build.sh
RUN bash ./scripts/build_auto_rsa.sh
RUN bash ./scripts/proto_build.sh

# Start command (Python 3.9 by default)
CMD ["python", "app/main.py"]