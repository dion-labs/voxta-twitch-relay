# Contributing

We welcome contributions to Voxta Twitch Relay!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/dion-labs/voxta-twitch-relay
   cd voxta-twitch-relay
   ```

2. Install dependencies using `uv`:
   ```bash
   uv sync --all-extras
   ```

3. Install pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```

## Running Tests

```bash
uv run pytest
```

## Linting and Formatting

We use `ruff` for linting and formatting.

```bash
uv run ruff check .
uv run ruff format .
```

## Building Documentation

```bash
uv run mkdocs serve
```
