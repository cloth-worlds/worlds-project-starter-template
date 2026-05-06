# Worlds Project Starter Template

A starter template for Worlds Python microservices using FastAPI, GraphQL (gql), and Pydantic Settings.

## Quick Start

1. Copy this template and rename the directory to your project name
2. Find and replace the following placeholders throughout the project:

| Placeholder | Replace With | Example |
|---|---|---|
| `my-project-name` | Your kebab-case project name | `seadrill-hard-hat` |
| `my_app` | Your Python package name (snake_case) | `shh_app` |
| `My Project Name` | Human-readable project name | `Seadrill Hard Hat` |

3. Update `helm/values.yaml` with your actual config/secret values
4. Update `.env.example` and create your `.env`
5. Run `uv sync` to install dependencies

## Project Structure

```
src/my_app/
  main.py              # FastAPI app entry point with lifespan
  core/
    config.py          # Pydantic BaseSettings (env vars)
    auth.py            # Bearer token authentication
    logger.py          # Logging configuration
    graphql/
      client.py        # GraphQL client (gql + aiohttp)
  api/
    routes.py          # API route stubs
tests/
helm/
  values.yaml          # Helm chart values
Dockerfile
pyproject.toml
```

## Development

```bash
uv sync                          # Install dependencies
uv run python -m my_app.main     # Run the app
uv run pytest                    # Run tests
uv run ruff check .              # Lint
```
