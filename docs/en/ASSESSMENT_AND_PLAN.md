# Assessment and Plan: Dockerization and Autotrading

This document outlines the possibilities for packaging the application in Docker and extending functionality to include true autotrading based on dynamic "confidence score".

## 1. Dockerization

### Assessment
Dockerizing this application is **highly appropriate**. It will make it easy to move the bot from your local machine to a cloud server (VM) without having to manually install Python, dependencies, or configure environment variables each time.

### Technical Solution
We need two files:
1.  **Dockerfile:** Defines the environment (Python 3.11), installs `requirements.txt`, and starts the app.
2.  **docker-compose.yml:** Defines the service, maps ports (8080), and most importantly: maps the `data/` volume so history and configuration survive restarts.

**Challenges:**
- **GUI on server:** NiceGUI runs on port 8080. On a server, this port must either be opened in the firewall or (better) run behind a reverse proxy (like Nginx) with password protection, since the NiceGUI app currently lacks built-in authentication.

---

## 2. Autotrading and Confidence Score

### Current Problem
You have observed that "Confidence" is always **75%**.
**Cause:** In `gemini_decision_maker.py`, we lack the `confidence` field in the JSON schema sent to the AI. Therefore, the bot doesn't know to provide it, and `bot_engine.py` uses "75.0" as a default value (backup).

### Solution for Autotrading
For autotrading to be safe, we must:
1.  **Update the AI Model:** Explicitly ask Gemini to assess confidence (0-100) based on signal strength (e.g., confluence between 5m and 4h charts).
2.  **Implement Threshold:** Add a `CONFIDENCE_THRESHOLD` setting (e.g., 80%).
3.  **Change Logic:**
    - If `confidence >= CONFIDENCE_THRESHOLD`: Execute trade automatically (Auto Mode).
    - If `confidence < CONFIDENCE_THRESHOLD`: Add as a "Proposal" requiring manual approval.

---

## 3. Implementation Plan

This work can be done in three phases to ensure stability.

| Phase | Task | Estimate | Description |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Dockerization** | 1 hour | Create Dockerfile and docker-compose. Test building locally. Ensure persistent data storage. |
| **Phase 2** | **Fix Confidence** | 1-2 hours | Update `gemini_decision_maker.py` JSON schema and System Prompt to include `confidence`. Verify we get varied scores (e.g., 60%, 85%, 92%) from Gemini. |
| **Phase 3** | **Autotrading Mode** | 2-3 hours | Implement logic in `bot_engine` checking the threshold. Add UI toggle for "Auto-Trade High Confidence Proposals". |

---

## 4. Test Plan

### Docker Test
1.  Run `docker-compose up --build`.
2.  Go to `localhost:8080`.
3.  Make a configuration change or add a "trade note".
4.  Stop the container and start it again.
5.  **Success Criteria:** The change persists (volume mapping works).

### Autotrading & Confidence Test
1.  Set `CONFIDENCE_THRESHOLD = 90` (very high).
2.  Let the bot run. Check logs.
3.  **Expectation:** See logs like *"Decision confidence 85% < 90%. Created proposal."* (No trade executed).
4.  Lower threshold to `CONFIDENCE_THRESHOLD = 50`.
5.  **Expectation:** Next signal (if confidence e.g. 70%) should execute immediately: *"Decision confidence 70% >= 50%. Executing AUTO trade."*
6.  **Safety Check:** Verify that the `max_position_size` guard we recently added still applies in auto-mode.

---

### Recommendation
I recommend starting with **Phase 2 (Fix Confidence)** first, as this adds immediate value to the current manual mode (you see how sure the AI is). Then Docker, and finally full Autotrading.
