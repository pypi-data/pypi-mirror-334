# Install uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

# Change the working directory to the `app` directory
WORKDIR /app

# Copy the lockfile and `pyproject.toml` into the image
COPY pyproject.toml /app/pyproject.toml

# Copy the project into the image
COPY . /app

# Sync the project
RUN uv sync

# Label associated repo
LABEL org.opencontainers.image.source https://github.com/GatlenCulp/gatpack

#