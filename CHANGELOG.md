# Changelog

## [Unreleased] - 2026-01-01

### Fixed
- **Docker Deployment Crash**: Resolved an issue where the application would crash in Docker because it attempted to launch a native desktop window (`pywebview`) in a headless environment.
    - **Removed Dependency**: Removed `pywebview` from `requirements.txt` as it is not needed for the server-side deployment.
    - **Forced Headless Mode**: Modified `main.py` to strictly enforce `native=False` and `show=False` when running in Docker, preventing any attempts to interact with a display server.
    - **Config Cleanup**: Removed deprecated `version` attribute from `docker-compose.yml` to suppress warnings.
    - **Startup Script**: Updated `scripts/start_bot.ps1` to correctly handle the rebuild process.

### Added
- **Startup Logging**: Added (and subsequently cleaned up) debug logging to verify correct environment mode detection (Headless vs Native).
