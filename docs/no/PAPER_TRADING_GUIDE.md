# 📄 Papirhandel Guide

Denne guiden forklarer hvordan du bruker **Papirhandel**-modus (Paper Trading) i Nof1.ai trading boten.
Papirhandel lar deg teste strategier og botens funksjonalitet **uten å risikere ekte penger**.

## 🚀 Hvordan fungerer det?

Papirhandel-backend erstatter den ekte Hyperliquid-tilkoblingen med en lokal simulering.
- **Priser**: Hentes i sanntid fra Binance (via offentlig API).
- **Ordre**: Simuleres lokalt (Limit, Market, TP/SL).
- **Saldo**: Starter med simulert $10,000 USDC.
- **Posisjoner**: Spores lokalt i `data/paper_trading_state.json`.

---

## 🛠️ Oppsett

1. **Konfigurer `.env`**:
   Sørg for at din `.env`-fil har følgende innstilling:
   ```properties
   TRADING_BACKEND=paper
   ```

2. **Ingen API-nøkler nødvendig**: 
   Siden det er simulert, trenger du ikke Hyperliquid-nøkler. Boten trenger bare internettilgang for å hente priser.

---

## ▶️ Kjøre boten

### **Metode 1: Bruke oppstartsskriptet (Anbefalt)**
Dobbeltklikk eller kjør `start_all.ps1`-skriptet i rotmappen.
```powershell
.\start_all.ps1
```
Dette vil starte både Backend (FastAPI) og Frontend (React).

### **Metode 2: Manuell start**

**Backend:**
```powershell
# Åpne terminal 1
python -m uvicorn src.api.main:app --reload
```

**Frontend:**
```powershell
# Åpne terminal 2
cd frontend
npm run dev
```

---

## 🖥️ Bruke grensesnittet

1. Åpne **http://localhost:5173** i nettleseren din.
2. Gå til **Dashboard**.
3. Du bør se en saldo på **$10,000**.
4. Du kan klikke "Start Bot" for å aktivere auto-trading (hvis konfigurert) eller handle manuelt via grensesnittet.

---

## 🧪 Nullstille simulering

For å nullstille saldo og posisjoner:
1. Stopp boten.
2. Slett tilstandsfilen:
   ```
   data/paper_trading_state.json
   ```
3. Start boten på nytt. Din saldo vil nullstilles til $10,000.

---

## 📝 Feilsøking

- **Priser er 0**: Sjekk internettilkoblingen din. Boten må kunne nå Binance API.
- **Ordre fylles ikke**: Limit-ordre fylles kun hvis markedsprisen krysser din limit-pris.
- **"Backend not connected"**: Sørg for at Python-backenden kjører.
