# 🚀 Gemini API Integration - Setup Guide

Dette dokumentet forklarer hvordan du bruker Google Gemini API med nof1.ai trading bot istedenfor OpenRouter.

---

## 📋 Innholdsfortegnelse

1. [Hvorfor Gemini?](#hvorfor-gemini)
2. [Forutsetninger](#forutsetninger)
3. [Installasjon](#installasjon)
4. [Konfigurasjon](#konfigurasjon)
5. [Testing](#testing)
6. [Feilsøking](#feilsøking)
7. [Sammenligning: Gemini vs OpenRouter](#sammenligning-gemini-vs-openrouter)

---

## 🎯 Hvorfor Gemini?

### Fordeler med direkte Gemini API:

✅ **Lavere kostnader:**
- Gemini 2.0 Flash: Gratis til Mai 2025
- Gemini 1.5 Pro: ~50% billigere enn via OpenRouter

✅ **Raskere responstid:**
- Ingen ekstra lag (direkte til Google)
- Typisk 200-500ms raskere

✅ **Context caching:**
- Gemini støtter caching av system prompts
- 75% rabatt på cached tokens
- Perfekt for trading bot (system prompt er stor og repeterende)

✅ **Læringsverdi:**
- Forstå hvordan LLM APIs fungerer
- Lær function calling / tool use
- Bygg erfaring med AI integrasjon

### Ulemper:

❌ **Kun én modell:**
- Kan ikke enkelt bytte til Claude/ChatGPT/Grok
- Må bruke OpenRouter for andre modeller

❌ **Ingen reasoning tokens:**
- Gemini har ikke "thinking mode" som o1/Grok

---

## 📦 Forutsetninger

### 1. Google Gemini API Key

**Gå til:** https://makersuite.google.com/app/apikey

**Steg:**
1. Logg inn med Google-konto
2. Klikk "Get API Key"
3. Kopier API-nøkkelen (begynner med `AIzaSy...`)

**Gratis tier:**
- 60 requests/minutt
- Gratis til Mai 2025 (Gemini 2.0 Flash)

### 2. Hyperliquid Testnet Wallet

**Hvorfor testnet først?**
- Null risiko - fake penger
- Identisk API som mainnet
- Lær uten stress

**Oppsett:**
```python
# Generer ny Ethereum wallet (Python)
from eth_account import Account
account = Account.create()
print(f"Private Key: {account.key.hex()}")
print(f"Address: {account.address}")
```

**Få testnet tokens:**
1. Join Hyperliquid Discord: https://discord.gg/hyperliquid
2. Gå til #testnet-faucet kanal
3. Send: `!faucet <din_wallet_address>`
4. Motta 10,000 USDC testnet tokens

### 3. TAAPI API Key (Valgfri)

**Gå til:** https://taapi.io

**Gratis tier:**
- 30 requests/måned
- Alle indikatorer tilgjengelig
- Nok for testing

**Alternativ (gratis uten API):**
- Bruk `pandas_ta` for lokal beregning
- Ingen external API-kall
- Må beregne indikatorer selv

---

## 🔧 Installasjon

### Steg 1: Installer Python dependencies

```bash
cd C:\Users\Rune\PycharmProjects\Nof1\nof1.ai-alpha-arena-nof1.ai-alpha-arena

# Installer alle dependencies (inkludert Gemini SDK)
pip install -r requirements.txt
```

**Viktige pakker som installeres:**
- `google-generativeai>=0.8.0` - Gemini SDK
- `hyperliquid-python-sdk` - Exchange API
- `nicegui>=2.0.0` - Desktop GUI

### Steg 2: Verifiser installasjon

```bash
python -c "import google.generativeai as genai; print('Gemini SDK installed:', genai.__version__)"
```

**Forventet output:**
```
Gemini SDK installed: 0.8.x
```

---

## ⚙️ Konfigurasjon

### Steg 1: Lag .env fil

```bash
# Kopier template
cp .env.example .env

# Rediger .env (bruk Notepad++ eller VS Code)
notepad .env
```

### Steg 2: Fyll inn minimal konfigurasjon

```env
# ============================================================================
# MINIMAL SETUP FOR GEMINI + TESTNET
# ============================================================================

# LLM Provider
LLM_PROVIDER=gemini

# Gemini API
GEMINI_API_KEY=AIzaSy...  # <-- DIN API KEY HER
GEMINI_MODEL=gemini-2.0-flash-exp

# Hyperliquid Testnet
HYPERLIQUID_NETWORK=testnet
HYPERLIQUID_PRIVATE_KEY=0xabc123...  # <-- DIN TESTNET PRIVATE KEY HER

# Trading Config
ASSETS=BTC,ETH
INTERVAL=5m
TRADING_MODE=manual  # <-- VIKTIG: Start med manual!

# TAAPI (valgfri - kan utelates for testing)
# TAAPI_API_KEY=your_key_here
```

### Steg 3: Verifiser konfigurasjon

```bash
python -c "from src.backend.config_loader import CONFIG; print('Provider:', CONFIG['llm_provider']); print('Model:', CONFIG['gemini_model'])"
```

**Forventet output:**
```
Provider: gemini
Model: gemini-2.0-flash-exp
```

---

## 🧪 Testing

### Test 1: Gemini API Connection

**Lag test-script:**

```python
# test_gemini.py
import google.generativeai as genai
from src.backend.config_loader import CONFIG

# Configure Gemini
genai.configure(api_key=CONFIG["gemini_api_key"])

# Create model
model = genai.GenerativeModel(CONFIG["gemini_model"])

# Test simple query
response = model.generate_content("Hei! Er du klar til å hjelpe med trading?")
print(response.text)
```

**Kjør:**
```bash
python test_gemini.py
```

**Forventet output:**
```
Ja! Jeg er klar til å hjelpe deg med trading. Jeg kan analysere
markedsdata, vurdere risiko, og foreslå trades basert på teknisk analyse...
```

### Test 2: Gemini Function Calling

**Test TAAPI tool calling:**

```python
# test_gemini_tools.py
import google.generativeai as genai
from src.backend.config_loader import CONFIG

genai.configure(api_key=CONFIG["gemini_api_key"])

# Define function
fetch_indicator = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="get_rsi",
            description="Fetch RSI indicator for BTC",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "symbol": genai.protos.Schema(type=genai.protos.Type.STRING)
                },
                required=["symbol"]
            )
        )
    ]
)

model = genai.GenerativeModel(CONFIG["gemini_model"])
chat = model.start_chat()

response = chat.send_message(
    "Hva er RSI for BTC?",
    tools=[fetch_indicator]
)

# Check if function was called
if response.candidates[0].content.parts[0].function_call:
    fc = response.candidates[0].content.parts[0].function_call
    print(f"✅ Gemini kalte funksjon: {fc.name}")
    print(f"   Argumenter: {dict(fc.args)}")
else:
    print("❌ Gemini kalte ikke funksjonen")
```

**Forventet output:**
```
✅ Gemini kalte funksjon: get_rsi
   Argumenter: {'symbol': 'BTC'}
```

### Test 3: Full Trading Decision (DRY RUN)

**Kjør bot i dry-run mode:**

```python
# test_trading_decision.py
import asyncio
from src.backend.agent.gemini_decision_maker import GeminiTradingAgent

async def test():
    agent = GeminiTradingAgent()

    # Mock market context
    context = """
    Current Time: 2025-01-15 14:30:00 UTC

    BTC:
    - Price: 98,500 USD
    - 5m RSI: 55
    - 4h MACD: Bullish crossover
    - Funding rate: 0.01%
    - Open Interest: Increasing

    ETH:
    - Price: 3,400 USD
    - 5m RSI: 62
    - 4h MACD: Bearish
    - Funding rate: 0.05%

    Account:
    - Balance: 10,000 USD
    - No active positions
    """

    result = agent.decide_trade(assets=["BTC", "ETH"], context=context)

    print("=" * 60)
    print("GEMINI REASONING:")
    print("=" * 60)
    print(result['reasoning'])
    print("\n" + "=" * 60)
    print("TRADE DECISIONS:")
    print("=" * 60)
    for decision in result['trade_decisions']:
        print(f"\n{decision['asset']}:")
        print(f"  Action: {decision['action'].upper()}")
        print(f"  Allocation: ${decision['allocation_usd']}")
        print(f"  TP: {decision['tp_price']}")
        print(f"  SL: {decision['sl_price']}")
        print(f"  Rationale: {decision['rationale']}")

asyncio.run(test())
```

**Kjør:**
```bash
python test_trading_decision.py
```

**Forventet output (eksempel):**
```
============================================================
GEMINI REASONING:
============================================================
Analyzing BTC: 4h MACD shows bullish crossover with neutral RSI (55).
This suggests early bullish momentum. Funding rate is low (0.01%),
indicating no overcrowding in longs. Open interest increasing confirms
fresh capital entering. Structure is supportive for LONG entry.

Analyzing ETH: Despite elevated RSI (62), 4h MACD is bearish and funding
rate is elevated (0.05%), suggesting overcrowded longs. Risk/reward
not favorable. Recommend HOLD until clearer setup.

============================================================
TRADE DECISIONS:
============================================================

BTC:
  Action: BUY
  Allocation: $500
  TP: 99500.0
  SL: 97500.0
  Rationale: Bullish MACD + low funding + OI increase = high probability setup

ETH:
  Action: HOLD
  Allocation: 0
  TP: None
  SL: None
  Rationale: Conflicting signals - wait for 4h MACD confirmation
```

### Test 4: Full Bot (GUI mode)

**Kjør hele applikasjonen:**

```bash
python main.py
```

**Hva skjer:**
1. GUI åpner i nettleser (http://localhost:3000)
2. Bot starter i background
3. Hver 5. minutt (INTERVAL=5m):
   - Henter markedsdata
   - Sender til Gemini for analyse
   - Viser forslag i GUI
4. I manual mode: Du godkjenner trades via GUI

**Sjekkliste:**
- [ ] GUI åpner uten errors
- [ ] Dashboard viser balance
- [ ] "Reasoning" page viser Gemini's analyse
- [ ] "Recommendations" page viser trade forslag
- [ ] Logs vises i `bot.log` og `llm_requests.log`

---

## 🔍 Feilsøking

### Problem 1: "GEMINI_API_KEY not found"

**Årsak:** .env fil mangler eller ikke lastet

**Løsning:**
```bash
# Sjekk at .env finnes
ls .env

# Sjekk innhold (Windows)
type .env

# Verifiser at key er satt
python -c "from src.backend.config_loader import CONFIG; print(CONFIG['gemini_api_key'])"
```

**Hvis None:**
- Sjekk at .env er i riktig mappe
- Sjekk at linjen er: `GEMINI_API_KEY=AIzaSy...` (ingen spaces rundt =)

### Problem 2: "Invalid API key"

**Årsak:** Feil API key eller utgått

**Løsning:**
1. Gå til https://makersuite.google.com/app/apikey
2. Generer ny key
3. Oppdater .env fil
4. Restart applikasjonen

### Problem 3: "Rate limit exceeded"

**Årsak:** For mange requests

**Gemini limits:**
- Free tier: 60 requests/minutt
- Paid tier: 1000 requests/minutt

**Løsning:**
- Øk INTERVAL (f.eks. fra 5m til 15m)
- Implementer caching (allerede i TAAPI client)
- Oppgrader til paid tier

### Problem 4: "Function calling not working"

**Symptomer:**
- Gemini returnerer svar uten å kalle TAAPI
- Ingen indikatorer i reasoning

**Debug:**
```python
# Legg til logging i gemini_decision_maker.py (linje ~200)
if response.candidates[0].content.parts[0].function_call:
    print("✅ Function call detected")
else:
    print("❌ No function call - Gemini chose not to use tools")
```

**Mulige årsaker:**
- System prompt for vag ("use tools if needed" → "use fetch_taapi_indicator for X")
- Context allerede inneholder alle nødvendige indikatorer
- Gemini model versjon støtter ikke function calling (eldre modeller)

### Problem 5: "JSON parse error"

**Symptomer:**
```
ERROR: JSON parse error: Expecting value: line 1 column 1 (char 0)
```

**Årsak:** Gemini returnerte ikke gyldig JSON

**Debug:**
```python
# Se fullstendig response i llm_requests.log
tail -f llm_requests.log  # Linux/Mac
Get-Content llm_requests.log -Wait  # Windows PowerShell
```

**Løsning:**
- Sjekk at `response_mime_type="application/json"` er satt
- Sjekk at schema er riktig definert
- Bruk fallback parsing (allerede implementert i gemini_decision_maker.py:305-315)

### Problem 6: "Hyperliquid testnet connection failed"

**Årsak:** Feil private key eller testnet er nede

**Løsning:**
```bash
# Test connection
python -c "
from src.backend.trading.hyperliquid_api import HyperliquidAPI
import asyncio

async def test():
    api = HyperliquidAPI()
    state = await api.get_user_state()
    print(f'Balance: {state[\"balance\"]} USDC')

asyncio.run(test())
"
```

**Forventet output:**
```
Balance: 10000.0 USDC
```

**Hvis error:**
- Sjekk at HYPERLIQUID_NETWORK=testnet
- Verifiser private key (0x prefix skal IKKE være der)
- Sjekk testnet status: https://app.hyperliquid-testnet.xyz

---

## 📊 Sammenligning: Gemini vs OpenRouter

### Kostnad (1 million tokens)

| Provider | Input | Output | Total |
|----------|-------|--------|-------|
| **Gemini 2.0 Flash (Direct)** | **$0** | **$0** | **$0** (til Mai 2025) |
| Gemini 2.0 Flash (OpenRouter) | $0 | $0 | $0 (free tier) |
| **Gemini 1.5 Pro (Direct)** | **$1.25** | **$5.00** | **$6.25** |
| Gemini 1.5 Pro (OpenRouter) | $2.50 | $10.00 | $12.50 |
| Grok 4 (OpenRouter) | $5.00 | $15.00 | $20.00 |
| Claude 3.7 Sonnet (OpenRouter) | $3.00 | $15.00 | $18.00 |

**Estimat for trading bot:**
- ~5,000 tokens per beslutning (system prompt + context + response)
- 288 beslutninger/dag (5min interval)
- ~1.4M tokens/dag

**Kostnad per dag:**
- Gemini 2.0 Flash (direkte): **$0**
- Gemini 1.5 Pro (direkte): **~$9/dag**
- Gemini via OpenRouter: **~$18/dag**

### Latency (gjennomsnitt)

| Provider | P50 | P95 | P99 |
|----------|-----|-----|-----|
| **Gemini Direct** | **800ms** | **1.2s** | **2.0s** |
| Gemini via OpenRouter | 1.2s | 2.0s | 3.5s |
| Grok via OpenRouter | 1.5s | 2.5s | 4.0s |

**Konklusjon:** Direkte Gemini er **30-40% raskere**

### Features

| Feature | Gemini Direct | OpenRouter |
|---------|---------------|------------|
| **Function calling** | ✅ Native | ✅ Normalized |
| **JSON mode** | ✅ response_schema | ✅ response_format |
| **Context caching** | ✅ 75% rabatt | ❌ Ikke tilgjengelig |
| **Reasoning tokens** | ❌ Ikke støttet | ⚠️ Kun o1/Grok |
| **Multi-model** | ❌ Kun Gemini | ✅ 200+ modeller |
| **Failover** | ❌ Kun Gemini | ✅ Automatisk fallback |

---

## 🎓 Neste Steg

### 1. Kjør på testnet (1-2 uker)
- [ ] Test i manual mode først
- [ ] Verifiser at Gemini's beslutninger gir mening
- [ ] Analyser reasoning output
- [ ] Godkjenn noen trades manuelt
- [ ] Observer utfall

### 2. Optimaliser prompts
- [ ] Eksperimenter med system prompt
- [ ] Juster risk management rules
- [ ] Legg til/fjern trading rules
- [ ] Test forskjellige leverage nivåer

### 3. Sammenlign modeller (valgfri)
- [ ] Test både Gemini og OpenRouter (Grok/Claude)
- [ ] Sammenlign decision quality
- [ ] Sammenlign kostnad vs ytelse
- [ ] Velg beste modell for ditt bruk

### 4. Bygg egen strategi
- [ ] Ekstraher komponenter til RobotTrader
- [ ] Lag custom trading logic
- [ ] Integrer med Hyperliquid API
- [ ] Test på paper trading

---

## 📚 Ressurser

### Offisiell Dokumentasjon
- **Gemini API:** https://ai.google.dev/gemini-api/docs
- **Function Calling:** https://ai.google.dev/gemini-api/docs/function-calling
- **Pricing:** https://ai.google.dev/pricing
- **Hyperliquid Docs:** https://hyperliquid.gitbook.io/hyperliquid-docs

### Lær mer
- **Google AI Studio:** https://makersuite.google.com (Test Gemini i browser)
- **Prompt Engineering:** https://ai.google.dev/gemini-api/docs/prompting-strategies
- **Safety Settings:** https://ai.google.dev/gemini-api/docs/safety-settings

### Feilsøking
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/google-gemini
- **GitHub Issues:** https://github.com/google/generative-ai-python/issues
- **Discord:** Hyperliquid Discord for testnet hjelp

---

## ✅ Sjekkliste: Klar til å trade?

Før du starter trading med ekte penger, sørg for at:

- [ ] Testet i testnet i minst 1 uke
- [ ] Verifisert at Gemini's decisions gir mening
- [ ] Forstår hvordan system prompt påvirker decisions
- [ ] Observert positive resultater i paper trading
- [ ] Satt TRADING_MODE=manual (vurder auto senere)
- [ ] Bruker DEDIKERT wallet (ikke main wallet)
- [ ] Starter med minimal kapital ($100-500)
- [ ] Har stoppfunksjoner (max drawdown, daily loss limit)
- [ ] Overvåker bot daglig første uken
- [ ] Har backup plan hvis bot feiler

---

**Lykke til med Gemini + nof1.ai trading bot! 🚀**

*For spørsmål eller problemer, opprett issue på GitHub.*
