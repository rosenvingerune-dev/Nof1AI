# 🚀 Testing Quick Start

Rask guide for å verifisere at Gemini-integrasjonen fungerer.

---

## ⚡ TL;DR - Kom i gang på 5 minutter

```bash
# 1. Installer dependencies
pip install -r requirements.txt

# 2. Lag .env fil
copy .env.example .env

# 3. Rediger .env med dine API keys
notepad .env

# 4. Kjør alle tester
python tests/test_all.py
```

Hvis alt er grønt ✅ → Du er klar til å trade!

---

## 📋 Før du starter

### Du trenger:

- [ ] **Gemini API Key**
  - Få gratis key: https://makersuite.google.com/app/apikey
  - Kopiér API-nøkkelen (starter med `AIzaSy...`)

- [ ] **Hyperliquid Testnet Wallet**
  - Generer ny Ethereum private key
  - Få testnet tokens fra Discord
  - Discord: https://discord.gg/hyperliquid

- [ ] **TAAPI Key** (valgfri)
  - Gratis tier: https://taapi.io
  - Nødvendig for tool calling test

---

## 🔧 Steg-for-steg Setup

### Steg 1: Generer Ethereum Wallet (for Hyperliquid testnet)

**Metode A: Python script**
```python
from eth_account import Account

# Generer ny wallet
account = Account.create()

print("=" * 60)
print("HYPERLIQUID TESTNET WALLET")
print("=" * 60)
print(f"Address: {account.address}")
print(f"Private Key: {account.key.hex()}")
print("\n⚠️  LAGRE PRIVATE KEY TRYGT!")
print("=" * 60)
```

**Metode B: Bruk eksisterende wallet**
- Bruk MetaMask eller annen Ethereum wallet
- **VIKTIG:** Bruk KUN testnet wallet, aldri main wallet!

### Steg 2: Få Testnet Tokens

1. Join Hyperliquid Discord: https://discord.gg/hyperliquid
2. Gå til `#testnet-faucet` kanal
3. Send kommando:
   ```
   !faucet YOUR_WALLET_ADDRESS
   ```
4. Vent ~30 sekunder
5. Du mottar 10,000 USDC testnet tokens

### Steg 3: Konfigurer .env

**Kopier template:**
```bash
copy .env.example .env
```

**Minimal konfigurasjon (.env):**
```env
# LLM Provider
LLM_PROVIDER=gemini

# Gemini
GEMINI_API_KEY=AIzaSy_YOUR_KEY_HERE
GEMINI_MODEL=gemini-2.0-flash-exp

# Hyperliquid Testnet
HYPERLIQUID_NETWORK=testnet
HYPERLIQUID_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE

# Trading
ASSETS=BTC,ETH
INTERVAL=5m
TRADING_MODE=manual
```

**Erstatt:**
- `AIzaSy_YOUR_KEY_HERE` → Din Gemini API key
- `0xYOUR_PRIVATE_KEY_HERE` → Din testnet private key

### Steg 4: Kjør Tester

**Alle tester (anbefalt):**
```bash
python tests/test_all.py
```

**Eller individuelt:**
```bash
python tests/test_01_environment.py      # ~5 sek
python tests/test_02_gemini_api.py       # ~15 sek
python tests/test_03_hyperliquid_api.py  # ~10 sek
python tests/test_04_gemini_trading_agent.py  # ~30 sek
```

---

## ✅ Forventet Output

### Hvis alt fungerer:

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
nof1.ai Gemini Integration - Complete Test Suite
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

====================================================================
Running: Environment Configuration
====================================================================

TEST 1: Environment Configuration
====================================================================

✓ LLM Provider: gemini

--- Gemini Configuration ---
✓ API Key: AIzaSy...abc4 (skjult)
✓ Model: gemini-2.0-flash-exp

--- Hyperliquid Configuration ---
✓ Network: testnet
✓ Using TESTNET (safe for learning)
✓ Private Key: 0xabc1...def9 (skjult)

--- Trading Configuration ---
✓ Assets: BTC,ETH
✓ Interval: 5m
✓ Trading Mode: manual
✓ MANUAL mode aktivert - trades krever godkjenning

====================================================================
TEST SUMMARY
====================================================================
✅ PASS: Environment loaded
✅ PASS: Gemini configuration
✅ PASS: Hyperliquid configuration
✅ PASS: Trading configuration

Total: 4/4 tests passed

🎉 All tests passed! Configuration looks good.

[... more tests ...]

====================================================================
COMPLETE TEST SUITE SUMMARY
====================================================================
✅ PASS: Environment Configuration
✅ PASS: Gemini API Connection
✅ PASS: Hyperliquid API Connection
✅ PASS: Gemini Trading Agent

Total: 4/4 test suites passed

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
ALL TESTS PASSED!
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

Your nof1.ai setup with Gemini is fully configured!

✅ Next steps:
   1. Review GEMINI_SETUP.md for usage instructions
   2. Start the bot: python main.py
   3. Test in MANUAL mode first
   4. Monitor trades in the GUI
```

---

## ❌ Vanlige Feil & Løsninger

### ❌ "GEMINI_API_KEY not found"

**Problem:** .env fil mangler eller ikke lastet

**Løsning:**
```bash
# Sjekk at .env eksisterer
dir .env

# Åpne og verifiser innhold
notepad .env

# Restart terminal etter .env endringer
```

### ❌ "Invalid API key"

**Problem:** Feil API key eller utgått

**Løsning:**
1. Gå til https://makersuite.google.com/app/apikey
2. Lag ny API key
3. Oppdater GEMINI_API_KEY i .env
4. Kjør test på nytt

### ❌ "Hyperliquid balance is 0"

**Problem:** Ingen testnet tokens

**Løsning:**
```bash
# 1. Join Discord
https://discord.gg/hyperliquid

# 2. I #testnet-faucet kanal:
!faucet YOUR_ADDRESS

# 3. Verifiser at du fikk tokens:
python tests/test_03_hyperliquid_api.py
```

### ❌ "ModuleNotFoundError: No module named 'google.generativeai'"

**Problem:** Gemini SDK ikke installert

**Løsning:**
```bash
pip install google-generativeai>=0.8.0
```

### ❌ "Rate limit exceeded"

**Problem:** For mange API-kall

**Løsning:**
- Vent 60 sekunder
- Gemini free tier: 60 requests/minutt
- Kjør tester saktere (én om gangen)

---

## 🎯 Test Breakdown

### Test 1: Environment (5 sekunder)
**Hva den gjør:**
- Sjekker at .env fil er riktig konfigurert
- Verifiserer API keys er satt
- Validerer trading konfigurasjon

**Kan feile hvis:**
- .env mangler
- API keys er placeholders
- Trading mode er ikke satt

### Test 2: Gemini API (15 sekunder)
**Hva den gjør:**
- Tester Gemini API tilkobling
- Verifiserer JSON structured output
- Tester function calling

**Kan feile hvis:**
- GEMINI_API_KEY er ugyldig
- Internett-tilkobling feiler
- API quota er oppbrukt

### Test 3: Hyperliquid API (10 sekunder)
**Hva den gjør:**
- Tester exchange API tilkobling
- Henter account balance
- Henter markedspriser

**Kan feile hvis:**
- Private key er feil
- Testnet er nede
- Ingen testnet funds

### Test 4: Trading Agent (30 sekunder)
**Hva den gjør:**
- Tester full trading decision flow
- Verifiserer AI reasoning
- Tester tool calling (hvis TAAPI)

**Kan feile hvis:**
- Test 1-3 feiler
- Gemini returnerer ugyldig JSON
- System prompt er for restriktiv

---

## 🔄 Hva skjer etter testene?

### ✅ Hvis alle tester passerer:

**Du er klar til å starte bot:**
```bash
python main.py
```

**GUI åpner på:** http://localhost:3000

**Første gang du kjører:**
1. Bot starter i background
2. Venter til første 5-minutt interval
3. Henter markedsdata
4. Sender til Gemini for analyse
5. Viser trade forslag i GUI
6. I manual mode: Du godkjenner via "Recommendations" page

### ❌ Hvis noen tester feiler:

**Ikke start bot ennå!**

1. Les feilmeldingen nøye
2. Fix problemet (se "Vanlige Feil" over)
3. Kjør testen på nytt
4. Når alle er grønne → Start bot

---

## 📚 Videre Lesing

- **GEMINI_SETUP.md** - Detaljert Gemini guide
- **tests/README.md** - Full test dokumentasjon
- **nof1AI_review.md** - Prosjektanalyse
- **.env.example** - Alle konfigurasjonsmuligheter

---

## 💡 Pro Tips

### Spar tid:

```bash
# Kjør kun tester som er relevante
python tests/test_02_gemini_api.py  # Kun Gemini

# Debugging: Enable verbose output
python -v tests/test_all.py
```

### Logging:

```bash
# Se Gemini API requests
type llm_requests.log

# Se bot activity
type bot.log

# Live monitoring (PowerShell)
Get-Content llm_requests.log -Wait

# ELLER (Anbefalt):
# Bruk "Logs" siden i Web GUI under "SYSTEM" menyen!
```

### Performance:

- Gemini 2.0 Flash: Gratis, rask (~1s response)
- Gemini 1.5 Pro: Betalt, bedre kvalitet (~2s response)
- Start med Flash, oppgrader hvis nødvendig

---

## 🆘 Trenger hjelp?

### Ressurser:

1. **Dokumentasjon**
   - Les GEMINI_SETUP.md
   - Sjekk tests/README.md

2. **Log filer**
   - llm_requests.log (Gemini errors)
   - bot.log (General errors)

3. **Community**
   - Hyperliquid Discord (testnet support)
   - Google AI Discord (Gemini support)

### Debugging checklist:

- [ ] .env fil eksisterer og er riktig formatert
- [ ] API keys er gyldige (ikke placeholders)
- [ ] Python 3.10+ installert
- [ ] Dependencies installert (requirements.txt)
- [ ] Internett-tilkobling fungerer
- [ ] Testnet wallet har funds (hvis testnet)

---

**Lykke til! 🚀**

*Start med test_all.py og følg instruksjonene. Du er klar på 5 minutter!*
