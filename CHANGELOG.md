# Changelog

## [Unreleased] - 2026-01-01

### Fixed
- **Docker Deployment Crash**: Resolved an issue where the application would crash in Docker because it attempted to launch a native desktop window (`pywebview`) in a headless environment.
    - **Removed Dependency**: Removed `pywebview` from `requirements.txt` as it is not needed for the server-side deployment.
    - **Forced Headless Mode**: Modified `main.py` to strictly enforce `native=False` and `show=False` when running in Docker, preventing any attempts to interact with a display server.
    - **Config Cleanup**: Removed deprecated `version` attribute from `docker-compose.yml` to suppress warnings.
    - **Startup Script**: Updated `scripts/start_bot.ps1` to correctly handle the rebuild process.
- **Graceful Shutdown**: Fixed an issue where stopping the bot in Docker would cause a Python `SystemExit` traceback.
    - Removed manual `signal.signal` handlers that were forcing `sys.exit(0)`.
    - Now relies on `NiceGUI` (Uvicorn) internal signal handling to trigger `app.on_shutdown` seamlessly.

### Added
- **Startup Logging**: Added (and subsequently cleaned up) debug logging to verify correct environment mode detection (Headless vs Native).

### Changed
- **Gemini SDK Migration**: Replaced the deprecated `google.generativeai` SDK with the new `google-genai` SDK (v0.2.0+).
    - Updated `src/backend/agent/gemini_decision_maker.py` to use the new client initialization, type definitions, and response parsing.
    - Updated `requirements.txt` to reflect the dependency change.
- **UI Performance Tuning**: Optimized dashboard responsiveness by reducing excessive WebSocket traffic.
    - Increased auto-refresh intervals for Dashboard, reasoning, and Recommendations pages from 2-3s to 10s.
    - Adjusted `binding_refresh_interval` in `main.py` from 0.1s to 0.5s to reduce server load.
    - Increased `reconnect_timeout` to improve stability.

### Fixed
- **UI Confidence Display**: Fixed a bug where confidence percentages were displaying as "0%" or "1%" due to decimal scaling errors (0.7 vs 70).
    - Added normalization logic in `src/gui/pages/recommendations.py` to correctly handle both 0-1 and 0-100 scales. 

