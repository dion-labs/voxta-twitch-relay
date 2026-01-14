FROM python:3.11-slim

# Install uv
COPY --from=astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN uv sync --frozen --no-dev

# Set the command
CMD ["uv", "run", "voxta-twitch-relay"]
