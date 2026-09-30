# Substrate Zero: The Full-Stack Cryptographic Substrate & Ephemeral Secret Failure Testbed
# Organization: @bootlace-dev
# Security Invariant: Zero-PII Container Image

FROM python:3.12-slim-bookworm

LABEL org.opencontainers.image.title="substrate-zero" \
      org.opencontainers.image.description="Where Cryptographic Mathematics Collide with Physical Reality" \
      org.opencontainers.image.url="https://github.com/bootlace-dev/substrate-zero" \
      org.opencontainers.image.authors="bootlace-dev@users.noreply.github.com" \
      org.opencontainers.image.source="https://github.com/bootlace-dev/substrate-zero"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TERM=xterm-256color

WORKDIR /opt/substrate-zero

# Install required system compilation and inspection toolchain
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    binutils \
    make \
    gdb \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies and source code
COPY requirements.txt setup.py ./
RUN pip install --no-cache-dir -r requirements.txt

COPY substrate_zero/ ./substrate_zero/
COPY scripts/ ./scripts/
COPY Makefile ./

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["python3", "-m", "substrate_zero.cli"]
CMD []
