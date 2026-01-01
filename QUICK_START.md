# ⚡ Quick Start Guide - nof1.ai med Gemini

3-minutters guide for å komme i gang med Gemini-drevet trading bot.

---

## 🎯 To alternativer for å starte

### 🟢 Alternativ A: Paper Trading (ANBEFALT - 100% gratis)
**Fordeler:**
- ✅ Ingen exchange account nødvendig
- ✅ Ingen wallet setup
- ✅ Ingen testnet tokens
- ✅ Start på 3 minutter
- ✅ 100% risikofritt (kun Gemini API nøkkel)

**Hva du trenger:**
- Gemini API key (gratis)
- Kun 3 minutter setup

**[Gå til Paper Trading Setup →](#paper-trading-setup)**

---

### 🟡 Alternativ B: Hyperliquid Testnet (Krever wallet)
**Fordeler:**
- ✅ Ekte exchange API
- ✅ Testnet (fake penger)
- ✅ Klar for mainnet senere

**Hva du trenger:**
- Gemini API key (gratis)
- Hyperliquid wallet med mainnet aktivitet
- 15-30 minutter setup

**[Gå til Hyperliquid Testnet Setup →](#hyperliquid-testnet-setup)**

---

## 🎯 Hva du får (begge alternativer)

- ✅ AI-drevet trading bot (Gemini 2.0 Flash)
- ✅ Real-time markedsdata
- ✅ Desktop GUI for monitoring
- ✅ Manual approval mode (du godkjenner trades)
- ✅ Full position tracking og PnL

---

# Paper Trading Setup

## 📋 Du trenger (2 minutter)

### 1. Gemini API Key (Gratis)
- Gå til: https://makersuite.google.com/app/apikey
- Klikk "Create API Key"
- Kopier nøkkelen (starter med `AIzaSy...`)

---

## 🚀 Setup (3 steg)

### Steg 1: Installer dependencies

```bash
cd C:\Users\Rune\PycharmProjects\Nof1\nof1.ai-alpha-arena-nof1.ai-alpha-arena
pip install -r requirements.txt
```

### Steg 2: Lag .env fil

```bash
# Kopier template
copy .env.example .env

# Åpne i editor
notepad .env
```

**Fyll inn (minimal konfig for PAPER TRADING):**
```env
# Trading Backend (VIKTIG!)
TRADING_BACKEND=paper

# Paper Trading (ingen exchange nødvendig!)
PAPER_TRADING_STARTING_BALANCE=10000.0

# LLM Provider
LLM_PROVIDER=gemini

# Gemini API
GEMINI_API_KEY=AIzaSy...  # <-- Din Gemini key her
GEMINI_MODEL=gemini-2.0-flash-exp

# Trading
ASSETS=BTC,ETH
INTERVAL=5m
TRADING_MODE=manual
```

### Steg 3: Test setup

```bash
# Test paper trading
python tests/test_05_paper_trading.py
```

**Forventet:**
```
✅ ALL PAPER TRADING TESTS PASSED!
   • Paper trading API initialized
   • Real-time prices from Binance
   • Order simulation working
```

---

## ▶️ Start Bot

```bash
python main.py
```

**GUI åpner på:** http://localhost:3000

**Du ser nå:**
- Dashboard med $10,000 simulated balance
- Real-time BTC/ETH prices fra Binance
- AI-genererte trading signals fra Gemini

**📚 Les mer:** `PAPER_TRADING_GUIDE.md` for fullstendig guide

---

# Hyperliquid Testnet Setup

**⚠️ MÅ ha wallet med mainnet aktivitet** - se `HYPERLIQUID_TESTNET_WORKAROUND.md`

## 📋 Du trenger

### 1. Gemini API Key (Gratis)
- Gå til: https://makersuite.google.com/app/apikey
- Klikk "Create API Key"
- Kopier nøkkelen (starter med `AIzaSy...`)

### 2. Hyperliquid Wallet
**OBS:** Du trenger en wallet som har vært aktiv på Hyperliquid mainnet!

**Alternativ 1: Bruk eksisterende MetaMask wallet**
- Hvis du har brukt Hyperliquid før
- Hent private key fra MetaMask
- Se `HYPERLIQUID_TESTNET_WORKAROUND.md`

**Alternativ 2: Generer ny wallet og aktiver den**
```bash
python scripts/setup_hyperliquid_testnet.py
```
- Koster $5-10 å aktivere på mainnet
- Se `HYPERLIQUID_TESTNET_WORKAROUND.md`

**Alternativ 3: Bruk paper trading istedet**
- 100% gratis
- Ingen wallet nødvendig
- Se [Paper Trading Setup](#paper-trading-setup)

---

## 🚀 Setup (4 steg)

### Steg 1: Installer dependencies

```bash
cd C:\Users\Rune\PycharmProjects\Nof1\nof1.ai-alpha-arena-nof1.ai-alpha-arena
pip install -r requirements.txt
```

### Steg 2: Sjekk wallet aktivering

```bash
python scripts/check_wallet_activation.py
```

Hvis **IKKE aktivert**, se `HYPERLIQUID_TESTNET_WORKAROUND.md` for løsninger.

### Steg 3: Lag .env fil

```bash
# Kopier template
copy .env.example .env

# Åpne i editor
notepad .env
```

**Fyll inn (minimal konfig for HYPERLIQUID TESTNET):**
```env
# Trading Backend
TRADING_BACKEND=hyperliquid

# Hyperliquid Testnet
HYPERLIQUID_NETWORK=testnet
HYPERLIQUID_PRIVATE_KEY=0x...  # <-- Din private key

# LLM Provider
LLM_PROVIDER=gemini

# Gemini API
GEMINI_API_KEY=AIzaSy...  # <-- Din Gemini key her
GEMINI_MODEL=gemini-2.0-flash-exp

# Trading
ASSETS=BTC,ETH
INTERVAL=5m
TRADING_MODE=manual
```

### Steg 4: Test setup

```bash
python tests/test_all.py
```

**Forventet:**
```
🎉 ALL TESTS PASSED!
```

---

## ▶️ Start Bot

```bash
python main.py
```

**GUI åpner på:** http://localhost:3000

---

## 📱 Bruk GUI

### Dashboard
- Account balance
- Total PnL
- Active positions
- Recent trades

### Reasoning
- Gemini's full analysis
- Market structure breakdown
- Decision rationale

### Recommendations
- Trade proposals (manual mode)
- Approve/reject each trade
- Risk/reward metrics

### Positions
- Active trades
- Entry/current price
- PnL per position
- TP/SL levels

---

## 🎓 Første Trading Sesjon

### 1. Start bot (manual mode)
```bash
python main.py
```

### 2. Vent på første analyse
- Bot kjører hvert 5. minutt (INTERVAL=5m)
- Henter markedsdata
- Sender til Gemini for analyse

### 3. Se Gemini's reasoning
- Gå til "Reasoning" page i GUI
- Les full analyse av markedet
- Forstå hvorfor AI foreslår trade

### 4. Review trade proposal
- Gå til "Recommendations" page
- Se foreslått trade (BUY/SELL/HOLD)
- Sjekk TP/SL priser
- Les rationale

### 5. Approve eller reject
- Klikk "Approve" hvis du er enig
- Klikk "Reject" hvis ikke
- Trade eksekverteres kun hvis godkjent

### 6. Monitor position
- Gå til "Positions" page
- Se PnL i real-time
- TP/SL triggers automatisk

---

## 💡 Tips for Første Uke

### Testing strategi:

**Dag 1-3: Observer**
- La boten kjøre uten å godkjenne trades
- Studer Gemini's reasoning
- Forstå hvordan AI tenker

**Dag 4-7: Selective trading**
- Godkjenn kun trades du er 100% enig i
- Start med små posisjoner ($100-500)
- Dokumenter resultater

**Uke 2: Mer aktiv**
- Øk posisjonsstørrelse til $500-1000
- Test flere assets (SOL, AVAX, etc.)
- Eksperimenter med leverage (3x maks)

---

## ⚙️ Justere Innstillinger

### Bytt assets:

**.env:**
```env
ASSETS=BTC,ETH,SOL
```

### Bytt intervall:

```env
INTERVAL=15m  # Mindre frekvente trades
# eller
INTERVAL=1h   # Kun 24 beslutninger/dag
```

### Bytt til auto mode (når komfortabel):

```env
TRADING_MODE=auto
```
⚠️ **ADVARSEL:** Auto mode eksekverterer trades uten godkjenning!

---

## 🔍 Troubleshooting

### "GEMINI_API_KEY not found"
```bash
# Sjekk at .env eksisterer
dir .env

# Verifiser innhold
type .env

# Restart terminal
```

### "No testnet funds"
```bash
# Sjekk balance
python scripts/check_testnet_balance.py

# Hvis $0, gå til Discord:
# 1. https://discord.gg/hyperliquid
# 2. #testnet-faucet kanal
# 3. !faucet YOUR_ADDRESS
```

### "Tests failing"
```bash
# Kjør individuelt for å isolere problem
python tests/test_01_environment.py
python tests/test_02_gemini_api.py
python tests/test_03_hyperliquid_api.py
python tests/test_04_gemini_trading_agent.py
```

---

## 📚 Dokumentasjon

### Kom i gang:
1. **QUICK_START.md** (dette dokumentet) ← Start her
2. **TESTING_QUICK_START.md** - Test guide
3. **HYPERLIQUID_TESTNET_GUIDE.md** - Testnet detaljer

### Dypere læring:
4. **GEMINI_SETUP.md** - Full Gemini guide
5. **nof1AI_review.md** - Prosjekt analyse
6. **IMPLEMENTATION_SUMMARY.md** - Teknisk oversikt

---

## ⚠️ Viktige Advarsler

### Før du starter:

- [ ] ✅ Du bruker TESTNET (ikke mainnet)
- [ ] ✅ TRADING_MODE=manual (ikke auto)
- [ ] ✅ Du har lest README-filene
- [ ] ✅ Du forstår at dette er læring/eksperimentering
- [ ] ✅ Du vet hvordan man stopper boten (Ctrl+C)

### Aldri gjør dette:

- ❌ Bruk testnet wallet på mainnet
- ❌ Commit .env til git
- ❌ Del private keys
- ❌ Start med auto mode
- ❌ Bruk ekte penger før grundig testing

---

## 🎯 Success Metrics

### Etter første uke, du bør ha:

- ✅ Kjørt 50+ trading cycles
- ✅ Forstått Gemini's reasoning pattern
- ✅ Godkjent og observert 5-10 trades
- ✅ Dokumentert win rate
- ✅ Identifisert forbedringspunkter

### Når klar for mainnet (om 2-4 uker):

- ✅ Konsistent profitt på testnet (>55% win rate)
- ✅ Forstår alle bot funksjoner
- ✅ Har testet error scenarios
- ✅ Komfortabel med risk management
- ✅ Starter med minimal kapital ($100-500)

---

## 🆘 Hjelp

### Ressurser:

1. **Dokumentasjon i prosjektet** (alle .md filer)
2. **Log filer:**
   - `bot.log` - Bot activity
   - `llm_requests.log` - Gemini API calls
   - `data/diary.jsonl` - Trade history

3. **Community:**
   - Hyperliquid Discord: https://discord.gg/hyperliquid
   - Google AI Discord (Gemini support)

---

## 🎉 Du er klar!

```bash
# Kjør disse kommandoene i rekkefølge:

# 1. Setup testnet wallet
python scripts/setup_hyperliquid_testnet.py

# 2. Få tokens fra Discord (følg instruksjoner)

# 3. Check balance
python scripts/check_testnet_balance.py

# 4. Kjør tester
python tests/test_all.py

# 5. Start bot
python main.py

# 6. Åpne browser: http://localhost:3000

# 7. Observer, lær, og ha det gøy! 🚀
```

---

**Lykke til med AI-trading! 🤖💰**

*Husk: Testnet er for læring. Ta deg tid, eksperimenter, og bli komfortabel før du vurderer mainnet.*
