# Home Assistant Add-On Dockerfile Template
# Reference: https://developers.home-assistant.io/docs/add-ons
#
# CRITICAL: Use official Home Assistant base images
# Do NOT use generic Alpine/Ubuntu images without understanding dependencies
#
# Home Assistant base images include:
# - S6 overlay (process management and init system)
# - bashio (helper functions for supervisor API)
# - Root filesystem compatibility

# Use {arch} placeholder for multi-architecture support
# Supported architectures: amd64, armv7, aarch64, armhf, i386
FROM ghcr.io/home-assistant/{arch}-base:latest

# Install system packages (Alpine Linux package manager)
RUN apk add --no-cache \
    python3 \
    py3-pip \
    ca-certificates

# Copy entire rootfs/ directory into image
# This includes S6 service definitions, configuration, application files
COPY rootfs /

# Set working directory (optional, for your application)
WORKDIR /app

# Install Python dependencies if your add-on uses Python
# RUN if [ -f requirements.txt ]; then \
#       pip install --no-cache-dir -r requirements.txt; \
#     fi

# Set user (security best practice - run as non-root if possible)
# USER appuser

# S6 overlay automatically starts services defined in rootfs/etc/s6-overlay/s6-rc.d/
# No need to specify CMD - S6 overlay handles process management
#
# Home Assistant automatically:
# - Passes SUPERVISOR_TOKEN environment variable
# - Sets up logging to stdout/stderr
# - Manages container lifecycle
# - Handles graceful shutdown on SIGTERM

# Health check (optional)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8080/health || exit 1

# Example: Application-specific setup
#
# If your add-on is Python-based:
# RUN pip install --no-cache-dir paho-mqtt requests
#
# If your add-on is Node.js-based:
# FROM ghcr.io/home-assistant/{arch}-base:latest
# RUN apk add --no-cache nodejs npm
# COPY rootfs /
# WORKDIR /app
# RUN npm install
#
# If your add-on needs system libraries:
# RUN apk add --no-cache \
#     libffi-dev \
#     openssl-dev \
#     gcc \
#     musl-dev
