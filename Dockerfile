# Generated by https://smithery.ai. See: https://smithery.ai/docs/config#dockerfile
# Start with a Python image that includes the uv tool pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS uv

# Set the working directory in the container
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy the project configuration and lockfile
COPY pyproject.toml uv.lock ./

# Install the project's dependencies without installing the project itself
RUN --mount=type=cache,target=/root/.cache/uv     uv sync --frozen --no-install-project --no-dev --no-editable

# Add the rest of the project source code
ADD src /app/src

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv     uv sync --frozen --no-dev --no-editable

# Define the entry point command to run the server
ENTRYPOINT ["uv", "run", "mcp-server-opensearch", "--opensearch-url", "http://localhost:9200", "--index-name", "my_index"]
