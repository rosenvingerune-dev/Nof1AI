# Vurdering og Plan: Dockerisering og Autotrading

Dette dokumentet beskriver mulighetene for å pakke applikasjonen i Docker og utvide funksjonaliteten til å inkludere ekte autotrading basert på dynamisk "confidence score".

## 1. Dockerisering

### Vurdering
Å dockerisere denne applikasjonen er **svært hensiktsmessig**. Det vil gjøre det enkelt å flytte boten fra din lokale maskin til en sky-server (VM) uten å måtte installere Python, dependencies eller konfigurere miljøvariabler manuelt hver gang.

### Teknisk Løsning
Vi trenger to filer:
1.  **Dockerfile:** Definerer miljøet (Python 3.11), installerer `requirements.txt`, og starter appen.
2.  **docker-compose.yml:** Definerer tjenesten, mapper porter (8080), og viktigst av alt: mapper volumet `data/` slik at historikk og konfigurasjon overlever omstart.

**Utfordringer:**
- **GUI på server:** NiceGUI kjører på port 8080. På en server må denne porten enten åpnes i brannmuren, eller (bedre) kjøres bak en reverse proxy (som Nginx) med passordbeskyttelse, siden NiceGUI-appen i dag mangler innebygd innlogging.

---

## 2. Autotrading og Confidence Score

### Problemet i dag
Du har observert at "Confidence" alltid er **75%**.
**Årsak:** I filen `gemini_decision_maker.py` mangler vi feltet `confidence` i JSON-skjemaet vi sender til AI-en. Boten vet derfor ikke hva den skal spørre om, og `bot_engine.py` bruker "75.0" som standardverdi (backup).

### Løsning for Autotrading
For at autotrading skal være trygt, må vi:
1.  **Oppdatere AI-modellen:** Be Gemini eksplisitt om å vurdere tillit (0-100) basert på hvor sterke signalene er (f.eks. samfall mellom 5m og 4h chart).
2.  **Implementere Terskel:** Legge til en innstilling `CONFIDENCE_THRESHOLD` (f.eks. 80%).
3.  **Endre Logikk:**
    - Hvis `confidence >= CONFIDENCE_THRESHOLD`: Utfør handelen automatisk (Auto Mode).
    - Hvis `confidence < CONFIDENCE_THRESHOLD`: Legg den til som et "Forslag" (Proposal) som du må godkjenne manuelt.

---

## 3. Fremdriftsplan

Dette arbeidet kan gjøres i tre faser for å sikre stabilitet.

| Fase | Oppgave | Estimat | Beskrivelse |
| :--- | :--- | :--- | :--- |
| **Fase 1** | **Dockerisering** | 1 time | Lage Dockerfile og docker-compose. Teste bygging lokalt. Sikre at data lagres persistent. |
| **Fase 2** | **Fikse Confidence** | 1-2 timer | Oppdatere `gemini_decision_maker.py` sitt JSON-skjema og System Prompt til å inkludere `confidence`. Verifisere at vi får varierte tall (f.eks. 60%, 85%, 92%) fra Gemini. |
| **Fase 3** | **Autotrading Modus** | 2-3 timer | Implementere logikken i `bot_engine` som sjekker terskelverdi. Legge til bryter i UI for "Auto-Trade High Confidence Proposals". |

---

## 4. Testplan

### Test av Docker
1.  Kjør `docker-compose up --build`.
2.  Gå til `localhost:8080`.
3.  Gjør en endring i konfigurasjon eller legg til en "trade note".
4.  Stopp containeren og start den igjen.
5.  **Suksesskriterie:** Endringen er der fortsatt (volum-mapping fungerer).

### Test av Autotrading & Confidence
1.  Stille inn `CONFIDENCE_THRESHOLD = 90` (veldig høyt).
2.  La boten kjøre. Sjekk logger.
3.  **Forventning:** Vi skal se logger som *"Decision confidence 85% < 90%. Created proposal."* (Ingen handel utført).
4.  Senk terskel til `CONFIDENCE_THRESHOLD = 50`.
5.  **Forventning:** Neste signal (hvis confidence f.eks. er 70%) skal utføres umiddelbart: *"Decision confidence 70% >= 50%. Executing AUTO trade."*
6.  **Sikkerhetssjekk:** Verifiser at `max_position_size` sperren vi nettopp laget fortsatt gjelder selv i auto-mode.

---

### Anbefaling
Jeg anbefaler at vi starter med **Fase 2 (Fikse Confidence)** først, siden dette gir verdi umiddelbart i dagens manuelle modus (du ser hvor sikker AI-en er). Deretter Docker, og til slutt full Autotrading.
