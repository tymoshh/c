# Stage 1: Build the virtual environment with uv
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

# Install Python 3.12
RUN uv python install 3.12

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Stage 2: Final image with Lighttpd
FROM debian:bookworm-slim

# Create group and user
RUN groupadd -g 1000 k24_c && \
    useradd -m -u 1000 -g k24_c -d /home/k24_c/mio mio

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        lighttpd \
        libcgi-pm-perl \
        default-mysql-client \
        && rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/k24_c/mio/.c \
             /var/run/lighttpd && \
    chown -R mio:k24_c /home/k24_c/mio /var/run/lighttpd

# Copy virtual environment from builder
COPY --from=builder --chown=mio:k24_c /app/ /home/k24_c/mio/.homepage/
COPY --from=builder --chown=python:python /python /python
USER mio
WORKDIR /home/k24_c/mio/.homepage/c
RUN mv /home/k24_c/mio/.homepage/src/* /home/k24_c/mio/.homepage/c
RUN echo "/home/k24_c/mio/.homepage/c/lib" > /home/k24_c/mio/.homepage/.venv/lib/python3.12/site-packages/dbcon.pth
RUN echo "export PATH=\$HOME/.homepage/.venv/bin:\$PATH" >> /home/k24_c/mio/.bashrc
RUN find ./ -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -exec chmod 644 {} \; && \
        find ./ -type f \( -name "*.cgi" -o -name "*.py" \) -exec chmod 700 {} \; && \
        find . -name "*.cgi" -type f  -exec chmod +x {} \; && \
        find . -name "*.py" -type f -exec chmod +x {} \; && \
        find . -type d -exec chmod 755 {} \; && \
        chmod +x run_cgi

USER root
# Copy Lighttpd configuration
COPY lighttpd.conf /etc/lighttpd/lighttpd.conf
COPY entrypoint.sh /entrypoint.sh
# Entrypoint script
RUN chmod +x /entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]