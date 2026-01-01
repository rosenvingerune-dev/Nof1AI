# 🛠️ Scripts - Utility Tools

Denne mappen inneholder hjelpescripts for setup og vedlikehold av nof1.ai trading bot.

---

## 📋 Tilgjengelige Scripts

### 1. 🏦 Hyperliquid Testnet Setup

**Fil:** `setup_hyperliquid_testnet.py`

**Formål:** Generer ny testnet wallet og vis instruksjoner for å få tokens

**Bruk:**
```bash
python scripts/setup_hyperliquid_testnet.py
```

**Hva den gjør:**
- ✅ Genererer ny Ethereum wallet
- ✅ Viser wallet address og private key
- ✅ Gir Discord faucet instruksjoner
- ✅ Hjelper med .env konfigurasjon
- ✅ Tilbyr å lagre wallet info til fil

**Output:**
```
======================================================================
HYPERLIQUID TESTNET WALLET GENERATOR
======================================================================

🔐 Genererer ny Ethereum wallet...

✅ Wallet generert!

======================================================================
WALLET INFORMASJON
======================================================================

📍 Address:
   0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1

🔑 Private Key:
   0xabc123...def789

======================================================================

⚠️  VIKTIG SIKKERHETSADVARSLER:
   1. Dette er en TESTNET wallet - bruk KUN til testing!
   2. ALDRI bruk denne på mainnet med ekte penger
   ...
```

**Når bruke:**
- Første gang du setter opp testnet
- Hvis du trenger ny testnet wallet
- Når du vil ha dedikert wallet for testing

---

### 2. 💰 Check Testnet Balance

**Fil:** `check_testnet_balance.py`

**Formål:** Verifiser at testnet wallet har mottatt tokens

**Bruk:**
```bash
python scripts/check_testnet_balance.py
```

**Hva den gjør:**
- ✅ Sjekker .env konfigurasjon
- ✅ Kobler til Hyperliquid testnet
- ✅ Henter account balance
- ✅ Viser open positions
- ✅ Henter markedsdata (prices, funding, OI)
- ✅ Gir clear status (funded eller ikke)

**Output (success):**
```
======================================================================
HYPERLIQUID TESTNET BALANCE CHECK
======================================================================

📋 Checking configuration...
✓ Network: testnet

🔌 Connecting to Hyperliquid testnet...
✓ Connected to: https://api.hyperliquid-testnet.xyz
✓ Wallet address: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1

💰 Fetching account balance...

======================================================================
ACCOUNT STATE
======================================================================

💵 Balance: $10,000.00 USDC
💎 Total Value: $10,000.00
📊 Open Positions: 0

======================================================================
STATUS
======================================================================

✅ Testnet wallet is funded!

   Balance: $10,000.00 USDC
   You can now start trading on testnet!
```

**Output (no funds):**
```
❌ No testnet funds found!

   You need to get testnet tokens from Discord faucet:

   1. Join: https://discord.gg/hyperliquid
   2. Go to #testnet-faucet channel
   3. Send: !faucet 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1
   4. Wait 10-30 seconds
   5. Run this script again to verify
```

**Når bruke:**
- Etter du har sendt faucet kommando
- For å verifisere at tokens ble mottatt
- Sjekke balance før trading
- Debug connection issues

---

### 3. 📊 Database Migration (Original)

**Fil:** `migrate_to_database.py`

**Formål:** Migrer trade data fra JSONL til SQLite database

**Bruk:**
```bash
python scripts/migrate_to_database.py
```

**Hva den gjør:**
- Leser `data/diary.jsonl`
- Konverterer til SQLite database
- Muliggjør SQL-queries på trade history

**Når bruke:**
- Hvis du vil bruke database istedenfor JSONL
- For avansert analytics
- Større datamengder (1000+ trades)

**Merk:** Dette er fra original nof1.ai prosjekt

---

## 🚀 Quick Start Workflow

### First-time Setup:

```bash
# Steg 1: Generer testnet wallet
python scripts/setup_hyperliquid_testnet.py

# Steg 2: Gå til Discord og få tokens
# (følg instruksjonene fra script)

# Steg 3: Verifiser at du fikk tokens
python scripts/check_testnet_balance.py

# Steg 4: Hvis balance er OK, kjør tester
python tests/test_all.py
```

### Daglig bruk:

```bash
# Check balance før trading
python scripts/check_testnet_balance.py

# Start bot
python main.py
```

---

## 📚 Relatert Dokumentasjon

- **HYPERLIQUID_TESTNET_GUIDE.md** - Komplett testnet guide
- **TESTING_QUICK_START.md** - Test setup guide
- **GEMINI_SETUP.md** - Gemini API setup
- **tests/README.md** - Test dokumentasjon

---

## 💡 Tips

### Wallet Management:

```bash
# Generer ny wallet
python scripts/setup_hyperliquid_testnet.py

# Lagre output til fil (tilbys av script)
# Fil: testnet_wallet.txt

# Kopier private key til .env
# HUSK: Slett testnet_wallet.txt etterpå!
del testnet_wallet.txt
```

### Balance Checking:

```bash
# Quick check
python scripts/check_testnet_balance.py

# Hvis du vil se mer detaljer
python tests/test_03_hyperliquid_api.py
```

### Debugging:

```bash
# Hvis check_testnet_balance feiler:

# 1. Sjekk .env
type .env

# 2. Verifiser network
# .env må ha: HYPERLIQUID_NETWORK=testnet

# 3. Verifiser private key format
# Må starte med: 0x
# Totalt 66 chars (0x + 64 hex)

# 4. Test API directly
python tests/test_03_hyperliquid_api.py
```

---

## 🔍 Troubleshooting

### Script fails to import modules

**Problem:**
```
ModuleNotFoundError: No module named 'eth_account'
```

**Løsning:**
```bash
pip install -r requirements.txt
```

### "No wallet credentials found"

**Problem:**
```
❌ No wallet credentials found!
```

**Løsning:**
1. Sjekk at .env eksisterer
2. Verifiser at en av disse er satt:
   - `HYPERLIQUID_PRIVATE_KEY=0x...`
   - `MNEMONIC=word1 word2 ...`

### "Invalid private key format"

**Problem:**
```
ValueError: Invalid HYPERLIQUID_PRIVATE_KEY format
```

**Løsning:**
1. Private key MÅ starte med `0x`
2. Totalt 66 chars (0x + 64 hex digits)
3. Ingen spaces, line breaks, eller andre tegn
4. Generer ny wallet hvis korrupt:
   ```bash
   python scripts/setup_hyperliquid_testnet.py
   ```

---

## ✅ Success Criteria

### setup_hyperliquid_testnet.py

Script lykkes hvis:
- ✅ Wallet genereres uten errors
- ✅ Address og private key vises
- ✅ Discord instruksjoner vises
- ✅ .env konfigurasjon forklares

### check_testnet_balance.py

Script lykkes hvis:
- ✅ Kobler til testnet
- ✅ Viser wallet address
- ✅ Henter balance ($10,000 USDC expected)
- ✅ Viser markedsdata (BTC/ETH prices)
- ✅ Gir clear next steps

---

## 🎯 Next Steps

Etter du har kjørt disse scriptene:

1. **Hvis testnet er funded:**
   ```bash
   python tests/test_all.py
   ```

2. **Hvis alle tester passerer:**
   ```bash
   python main.py
   ```

3. **Observer trading i GUI:**
   - http://localhost:3000
   - Dashboard page: Account overview
   - Reasoning page: Gemini's analysis
   - Recommendations page: Trade proposals (manual mode)

---

**Happy testing! 🚀**
