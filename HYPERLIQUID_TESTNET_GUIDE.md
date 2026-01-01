# 🏦 Hyperliquid Testnet - Komplett Setup Guide

Denne guiden viser deg hvordan du setter opp Hyperliquid testnet for å teste trading bot uten risiko.

---

## 📋 Hva er Hyperliquid Testnet?

### Testnet vs Mainnet

| Feature | Testnet | Mainnet |
|---------|---------|---------|
| **Penger** | Fake tokens (gratis) | Ekte penger ($) |
| **Risiko** | 0% - kan ikke tape penger | 100% - kan tape alt |
| **API** | Identisk som mainnet | Produksjons-API |
| **Trading** | Full funksjonalitet | Full funksjonalitet |
| **Perfekt for** | Læring, testing, debugging | Live trading |

### Hvorfor bruke testnet først?

✅ **Lær uten risiko**
- Test strategier uten å risikere ekte penger
- Forstå hvordan boten fungerer
- Eksperimenter med leverage og posisjonsstørrelse

✅ **Verifiser setup**
- Sjekk at API-integrasjonen fungerer
- Test Gemini trading decisions
- Validér TP/SL mekanikk

✅ **Debug i fred**
- Finn bugs før live trading
- Test extreme scenarios
- Lær av feil uten kostnad

---

## 🚀 Quick Start (10 minutter)

### Steg 1: Generer Testnet Wallet

**Automatisk (anbefalt):**
```bash
cd C:\Users\Rune\PycharmProjects\Nof1\nof1.ai-alpha-arena-nof1.ai-alpha-arena
python scripts/setup_hyperliquid_testnet.py
```

**Manuelt (Python):**
```python
from eth_account import Account

# Generer ny wallet
account = Account.create()

print(f"Address: {account.address}")
print(f"Private Key: {account.key.hex()}")

# LAGRE DISSE TRYGT!
```

**Output:**
```
Address: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1
Private Key: 0xabc123...def789
```

### Steg 2: Få Testnet Tokens

**Join Discord:**
1. Gå til: https://discord.gg/hyperliquid
2. Godta server-reglene
3. Finn `#testnet-faucet` kanal

**Send kommando:**
```
!faucet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1
```
*(Bytt ut med din wallet address)*

**Respons (innen 30 sekunder):**
```
✅ Sent 10,000 USDC to 0x742d35...0bEb1
```

### Steg 3: Konfigurer .env

**Åpne .env:**
```bash
notepad .env
```

**Legg til:**
```env
# Hyperliquid Testnet
HYPERLIQUID_NETWORK=testnet
HYPERLIQUID_PRIVATE_KEY=0xabc123...def789
```

### Steg 4: Verifiser Setup

**Sjekk balance:**
```bash
python scripts/check_testnet_balance.py
```

**Forventet output:**
```
✅ Testnet wallet is funded!
   Balance: $10,000.00 USDC
   You can now start trading on testnet!
```

---

## 🔐 Sikkerhet

### Viktige Regler:

⚠️ **ALDRI bruk testnet wallet på mainnet**
- Testnet private keys er ofte lagret usikkert
- Bruk KUN for testing

⚠️ **ALDRI bruk mainnet wallet på testnet**
- Kan føre til forvirring
- Risiko for å sende ekte penger til testnet

⚠️ **Lag dedikerte wallets**
- Testnet wallet: Kun for testing
- Mainnet wallet: Kun for live trading
- Lagre hver separat

### Best Practices:

✅ **Wallet hygiene:**
```
Testnet Wallet (generert av script)
  ↓
.env fil (HYPERLIQUID_NETWORK=testnet)
  ↓
ALDRI bruk denne på mainnet

Mainnet Wallet (separat, sikker)
  ↓
Annen .env eller config
  ↓
ALDRI bruk denne på testnet
```

✅ **Git safety:**
- .env er i .gitignore ✅
- ALDRI commit private keys
- ALDRI push .env til GitHub

---

## 🧪 Testing Flow

### Anbefalt testprosess:

```
1. Generer testnet wallet
   ↓
2. Få testnet tokens (Discord)
   ↓
3. Verifiser balance ($10,000 USDC)
   ↓
4. Kjør API-tester (test_03_hyperliquid_api.py)
   ↓
5. Kjør full test suite (test_all.py)
   ↓
6. Start bot i MANUAL mode
   ↓
7. Observer AI-beslutninger
   ↓
8. Godkjenn noen trades manuelt
   ↓
9. Analyser resultater
   ↓
10. Juster strategi
   ↓
11. Repeat (1-2 uker på testnet)
   ↓
12. Når komfortabel → Vurder mainnet (med forsiktighet!)
```

---

## 📊 Testnet Features

### Hva fungerer på testnet:

✅ **Full trading funksjonalitet:**
- Market orders
- Limit orders
- Take-profit orders
- Stop-loss orders
- Position management

✅ **Markedsdata:**
- Real-time prices (synced med mainnet)
- Funding rates
- Open interest
- Order books

✅ **Account management:**
- Balance tracking
- PnL calculation
- Margin calculations
- Liquidation mechanics

### Forskjeller fra mainnet:

⚠️ **Liquiditet:**
- Testnet har mindre likviditet
- Større slippage på store orders
- Færre motparter

⚠️ **Funding rates:**
- Kan være forskjellig fra mainnet
- Mindre trading volume → mer volatile funding

⚠️ **Performance:**
- Kan være tregere enn mainnet
- Mindre reliable (testnet kan gå ned)

---

## 🔍 Troubleshooting

### Problem: "Insufficient balance"

**Symptom:**
```
❌ No testnet funds found!
   Balance: $0.00 USDC
```

**Løsning:**
1. Sjekk at du sendte Discord kommando:
   ```
   !faucet YOUR_ADDRESS
   ```
2. Vent 30-60 sekunder
3. Kjør balance check igjen
4. Hvis fortsatt $0:
   - Prøv Discord kommando på nytt
   - Spør i #testnet-support kanal

### Problem: "Invalid private key"

**Symptom:**
```
❌ Failed to initialize API: Invalid private key format
```

**Løsning:**
1. Sjekk at private key starter med `0x`
2. Verifiser at det er 66 tegn totalt (0x + 64 hex chars)
3. Ingen spaces eller line breaks
4. Generer ny wallet hvis korrupt:
   ```bash
   python scripts/setup_hyperliquid_testnet.py
   ```

### Problem: "Connection failed"

**Symptom:**
```
❌ Failed to fetch balance: Connection error
```

**Løsning:**
1. Sjekk internett-tilkobling
2. Verifiser at `HYPERLIQUID_NETWORK=testnet` i .env
3. Sjekk testnet status:
   - https://status.hyperliquid.xyz
   - Hyperliquid Discord #testnet-status
4. Prøv igjen om 5 minutter

### Problem: "Testnet er nede"

**Symptom:**
```
⚠️  Hyperliquid testnet might be down
```

**Løsning:**
1. Gå til Discord #testnet-status
2. Sjekk om andre har samme problem
3. Vent på at testnet kommer opp igjen
4. Testnet er ikke 100% uptime garantert
5. Kan fortsette med andre tester (Gemini API etc.)

---

## 💡 Tips & Tricks

### Få mest ut av testnet:

**1. Start med små posisjoner**
```
Selv om det er fake penger, test som om det var ekte:
- Start med $100-500 posisjoner
- Øk gradvis til $1000-2000
- Test max $5000 per trade
```

**2. Test edge cases**
```python
# Test ekstreme scenarios:
- Høy leverage (10x)
- Veldig små posisjoner ($10)
- Mange samtidige posisjoner
- Rapid position flipping
```

**3. Analyser AI-beslutninger**
```
Observer Gemini's reasoning:
- Hvorfor velger den BUY vs SELL?
- Er TP/SL fornuftige?
- Følger den trading rules?
- Respekterer den cooldowns?
```

**4. Dokumenter læring**
```
Hold en trading journal:
- Hva fungerte?
- Hva fungerte ikke?
- Hvilke prompts ga best resultater?
- Hvor ofte var AI riktig?
```

### Testnet Limitations:

⚠️ **Husk:**
- Testnet resultater != mainnet resultater
- Mindre liquiditet = mer slippage
- Funding rates kan være kunstige
- Ikke samme psykologi (fake penger)

### Når bytte til mainnet:

✅ **Klar for mainnet når:**
- [ ] Testet i 1-2 uker på testnet
- [ ] Forstår alle bot-funksjoner
- [ ] Observert konsistent profitt på testnet
- [ ] Komfortabel med AI-beslutninger
- [ ] Vet hvordan man stopper boten i nødsituasjoner
- [ ] Har satt opp alerts/monitoring
- [ ] Starter med minimal kapital ($100-500)

---

## 📚 Ressurser

### Hyperliquid Dokumentasjon:

- **Testnet App:** https://app.hyperliquid-testnet.xyz
- **Docs:** https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/testnet
- **API Docs:** https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api
- **Discord:** https://discord.gg/hyperliquid
- **Status:** https://status.hyperliquid.xyz

### Nyttige Discord Kanaler:

- `#testnet-faucet` - Få tokens
- `#testnet-support` - Hjelp med problemer
- `#testnet-status` - Testnet uptime/issues
- `#dev-chat` - Utvikler-diskusjoner
- `#api-support` - API-spesifikke spørsmål

---

## 🎯 Testnet Workflow

### Daglig testing routine:

```bash
# Morgen - Sjekk status
python scripts/check_testnet_balance.py

# Start bot i MANUAL mode
python main.py

# Observer trades gjennom dagen
# - Sjekk "Reasoning" page i GUI
# - Review trade proposals
# - Godkjenn selektivt

# Kveld - Analyser resultater
# - Gjennomgå diary.jsonl
# - Sjekk win rate
# - Evaluer Gemini's decisions

# Juster strategi
# - Endre system prompt hvis nødvendig
# - Tweake risk parameters
# - Test nye indikatorer
```

---

## ✅ Quick Reference

### Kommandoer du trenger:

```bash
# Setup (én gang)
python scripts/setup_hyperliquid_testnet.py

# Check balance (når som helst)
python scripts/check_testnet_balance.py

# Test API (etter setup)
python tests/test_03_hyperliquid_api.py

# Start trading (når klar)
python main.py
```

### .env konfigurasjon:

```env
# Testnet (start her)
HYPERLIQUID_NETWORK=testnet
HYPERLIQUID_PRIVATE_KEY=0x...

# Mainnet (SENERE, når erfaren)
# HYPERLIQUID_NETWORK=mainnet
# HYPERLIQUID_PRIVATE_KEY=0x...  # ANNEN WALLET!
```

### Discord kommandoer:

```
# Få tokens (én gang per wallet)
!faucet YOUR_ADDRESS

# Sjekk faucet status
!faucet status

# Hjelp
!faucet help
```

---

## 🆘 Trenger Hjelp?

### Feilsøking steg-for-steg:

1. **Sjekk .env konfigurasjon:**
   ```bash
   type .env
   # Verifiser: HYPERLIQUID_NETWORK=testnet
   ```

2. **Test wallet:**
   ```bash
   python scripts/check_testnet_balance.py
   ```

3. **Test API:**
   ```bash
   python tests/test_03_hyperliquid_api.py
   ```

4. **Se logger:**
   ```bash
   type bot.log
   ```

5. **Spør i Discord:**
   - #testnet-support kanal
   - Beskriv problemet + feilmelding
   - Inkluder wallet address (IKKE private key!)

---

**Lykke til med testnet trading! 🚀**

*Husk: Testnet er for læring. Ta deg tid, eksperimenter, og ha det gøy!*
