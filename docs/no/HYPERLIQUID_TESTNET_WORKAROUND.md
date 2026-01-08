# 🚧 Hyperliquid Testnet Faucet Problem & Løsninger

## ❌ Problemet: "User does not exist on mainnet"

Hyperliquid testnet faucet har en anti-spam regel:

**Du kan KUN få testnet tokens hvis wallet-adressen din har vært aktiv på Hyperliquid MAINNET først.**

Dette betyr:
- Nye wallets (generert av vårt setup script) fungerer IKKE
- Du må ha en wallet som allerede har gjort minst én transaksjon på Hyperliquid mainnet

---

## ✅ Løsninger (3 alternativer)

### 🎯 Alternativ 1: Bruk eksisterende wallet (Anbefalt hvis du har en)

**Hvis du allerede har en MetaMask/Rabby wallet som du har brukt på Hyperliquid:**

#### Steg 1: Hent private key fra MetaMask
```
1. Åpne MetaMask
2. Klikk på account menu (3 prikker)
3. Account details → Show private key
4. Skriv inn password
5. Kopier private key
```

#### Steg 2: Legg i .env
```env
HYPERLIQUID_NETWORK=testnet
HYPERLIQUID_PRIVATE_KEY=0x...  # <-- Din eksisterende wallet
```

#### Steg 3: Få testnet tokens
```
1. Gå til https://app.hyperliquid-testnet.xyz
2. Connect wallet (samme som i .env)
3. Claim faucet
4. Få 10,000 USDC testnet tokens
```

**Fordeler:**
- ✅ Fungerer umiddelbart
- ✅ Ingen ekstra steg

**Ulemper:**
- ⚠️ Bruker din main wallet (men på testnet, så trygt)
- ⚠️ Må ha brukt Hyperliquid før

---

### 🎯 Alternativ 2: Aktiver ny wallet på mainnet (Koster ~$5-10)

**Hvis du vil ha dedikert bot-wallet:**

#### Steg 1: Send litt USDC til ny wallet
```
1. Kjøp/få USDC på Arbitrum
2. Send $5-10 til bot-wallet: 0x523FD94f8f1571C75c916Cf2Fc936B8E371a946a
3. Gå til https://app.hyperliquid.xyz (MAINNET)
4. Connect wallet
5. Gjør én liten trade (f.eks. kjøp $1 verdi BTC)
6. Nå er wallet "aktivert"
```

#### Steg 2: Bruk testnet faucet
```
1. Gå til https://app.hyperliquid-testnet.xyz
2. Connect samme wallet
3. Claim faucet
4. Få 10,000 USDC testnet tokens
```

**Fordeler:**
- ✅ Dedikert wallet kun for bot
- ✅ Klar for både testnet og mainnet

**Ulemper:**
- ❌ Koster ekte penger (~$5-10)
- ❌ Må vente på transaksjoner

---

### 🎯 Alternativ 3: Bruk annen testnet exchange (0 kr, men annen platform)

**Hvis du ikke vil bruke ekte penger eller main wallet:**

Det finnes andre exchanges med paper trading:

#### A) Binance Testnet (Gratis, enkel)
- https://testnet.binance.vision/
- Få gratis testnet BTC/ETH/USDT
- CCXT library støtter Binance testnet
- Krever modifisering av bot (bytt fra Hyperliquid til Binance)

#### B) Bybit Testnet (Gratis)
- https://testnet.bybit.com/
- Automatisk får 1 BTC testnet
- Perpetual futures trading
- Krever modifisering av bot

#### C) Paper Trading API (Fullt simulert)
Lag en mock API som simulerer Hyperliquid uten ekte exchange:
```python
# paper_trading_api.py
class PaperTradingAPI:
    def __init__(self, starting_balance=10000):
        self.balance = starting_balance
        self.positions = {}
        # Hent real-time prices fra CoinGecko/Binance
        # Simuler trades lokalt
```

**Fordeler:**
- ✅ 100% gratis
- ✅ Full kontroll
- ✅ Kan teste extreme scenarios

**Ulemper:**
- ❌ Krever kode-endringer
- ❌ Ikke "ekte" exchange API
- ❌ Må bygge egen simulering

---

## 🎯 Min Anbefaling

### Hvis du har MetaMask og har brukt Hyperliquid før:
→ **Alternativ 1** (bruk eksisterende wallet)

### Hvis du aldri har brukt Hyperliquid:
→ **Alternativ 2** (aktiver wallet på mainnet med $5)

### Hvis du vil teste 100% gratis:
→ **Alternativ 3** (bytt til Binance testnet eller lag paper trading)

---

## 📝 Steg-for-steg: Alternativ 1 (Bruk eksisterende wallet)

### 1. Hent private key fra MetaMask

**Windows/Mac:**
1. Åpne MetaMask extension
2. Klikk på account icon (øverst til høyre)
3. Velg "Account details"
4. Klikk "Show private key"
5. Skriv inn MetaMask password
6. Klikk "Confirm"
7. **KOPIER private key** (64 hex chars)

### 2. Oppdater .env

```env
# Erstatt denne linjen:
# HYPERLIQUID_PRIVATE_KEY=0x...  # Fra setup script

# Med din MetaMask private key:
HYPERLIQUID_PRIVATE_KEY=0x1a2b3c4d5e6f...  # <-- Fra MetaMask
```

### 3. Test connection

```bash
python scripts/check_testnet_balance.py
```

**Forventet (første gang):**
```
✓ Wallet address: 0xYourMetaMaskAddress
❌ No testnet funds found!
   Balance: $0.00 USDC
```

### 4. Claim testnet tokens (via web UI)

**Ikke Discord faucet - bruk web UI:**

1. Gå til: https://app.hyperliquid-testnet.xyz
2. Klikk "Connect Wallet"
3. Velg MetaMask
4. Godkjenn connection
5. Klikk på wallet address (øverst til høyre)
6. Klikk "Faucet" eller "Get Testnet Tokens"
7. Klikk "Claim"
8. Vent 10 sekunder

### 5. Verifiser at du fikk tokens

```bash
python scripts/check_testnet_balance.py
```

**Forventet:**
```
✅ Testnet wallet is funded!
   Balance: $10,000.00 USDC
```

### 6. Kjør tester

```bash
python tests/test_all.py
```

### 7. Start bot

```bash
python main.py
```

---

## 📝 Steg-for-steg: Alternativ 2 (Aktiver ny wallet)

### 1. Kjøp USDC på Arbitrum

**Hvis du ikke har USDC:**

#### Via CEX (Centralized Exchange):
1. Kjøp USDC på Binance/Coinbase
2. Withdraw til Arbitrum network
3. Send til bot-wallet: `0x523FD94f8f1571C75c916Cf2Fc936B8E371a946a`

#### Via DEX (Decentralized Exchange):
1. Bridge ETH til Arbitrum via https://bridge.arbitrum.io/
2. Swap ETH → USDC på Uniswap (Arbitrum)
3. Send til bot-wallet

### 2. Aktiver wallet på Hyperliquid mainnet

```
1. Gå til: https://app.hyperliquid.xyz (MAINNET!)
2. Connect wallet (0x523...)
3. Deposit $5-10 USDC
4. Gjør én liten trade:
   - Asset: BTC
   - Size: $1 verdi
   - Side: Long eller Short (irrelevant)
5. Close position umiddelbart
6. Nå er wallet "aktivert" i Hyperliquid system
```

### 3. Bruk testnet faucet

```
1. Gå til: https://app.hyperliquid-testnet.xyz
2. Connect wallet (samme 0x523...)
3. Claim faucet
4. Få 10,000 USDC testnet tokens
```

### 4. Verifiser

```bash
python scripts/check_testnet_balance.py
```

---

## 🔧 Oppdatert Setup Script

Jeg har laget et nytt script som sjekker om wallet er aktivert:

```bash
python scripts/check_wallet_activation.py
```

Dette scriptet vil:
- ✅ Sjekke om wallet eksisterer på mainnet
- ✅ Fortelle deg om du kan bruke testnet faucet
- ✅ Gi deg alternativene over hvis ikke aktivert

---

## ⚠️ Viktig Sikkerhet

### Hvis du bruker eksisterende wallet (Alternativ 1):

**Forsiktighetsmomenter:**
- ⚠️ Samme private key brukes på både testnet og mainnet
- ⚠️ Pass på at `HYPERLIQUID_NETWORK=testnet` i .env
- ⚠️ ALDRI bytt til mainnet uten å være 100% sikker

**Sikkerhetstips:**
```env
# DOBBELTSJEKK at dette står i .env:
HYPERLIQUID_NETWORK=testnet  # TESTNET!!!

# IKKE endre til mainnet med mindre du VET hva du gjør:
# HYPERLIQUID_NETWORK=mainnet  # ❌ FARLIG hvis du eksperimenterer
```

### Best practice:

**Lag to .env filer:**
```bash
# .env.testnet (for testing)
HYPERLIQUID_NETWORK=testnet
HYPERLIQUID_PRIVATE_KEY=0x...  # Kan være main wallet

# .env.mainnet (for live trading - SENERE!)
HYPERLIQUID_NETWORK=mainnet
HYPERLIQUID_PRIVATE_KEY=0x...  # ANNEN wallet, kun for trading
```

**Bruk riktig .env:**
```bash
# Testing:
copy .env.testnet .env
python main.py

# Live (mye senere, når klar):
copy .env.mainnet .env
python main.py
```

---

## 💡 Hva jeg anbefaler FOR DEG

Basert på at du vil lære og teste:

### 🎯 Min anbefaling: Alternativ 1 (hvis du har MetaMask)

**Fordeler for deg:**
1. ✅ Raskest å komme i gang (5 minutter)
2. ✅ Gratis
3. ✅ Kan starte testing umiddelbart
4. ✅ Kun testnet - ingen risiko for ekte penger

**Prosess:**
```bash
# 1. Hent private key fra MetaMask
# 2. Legg i .env
# 3. Gå til https://app.hyperliquid-testnet.xyz
# 4. Connect wallet og claim faucet
# 5. Kjør: python scripts/check_testnet_balance.py
# 6. Kjør: python tests/test_all.py
# 7. Start: python main.py
```

### 🎯 Hvis du IKKE har MetaMask eller aldri brukt Hyperliquid:

**Da anbefaler jeg Alternativ 3: Lag paper trading API**

Jeg kan hjelpe deg å lage en enkel simulert exchange:
- Henter real-time prices fra CoinGecko
- Simuler trades lokalt
- Ingen ekte exchange nødvendig
- 100% gratis
- Full kontroll

**Vil du at jeg lager paper trading API for deg?**

---

## 🆘 Hva vil du gjøre?

Fortell meg:
1. **Har du MetaMask eller annen wallet du har brukt før?**
   - Ja → Alternativ 1
   - Nei → Gå til #2

2. **Er du villig til å bruke $5-10 for å aktivere wallet?**
   - Ja → Alternativ 2
   - Nei → Gå til #3

3. **Vil du teste uten ekte exchange?**
   - Ja → Jeg lager paper trading API
   - Nei → Vurder Binance testnet

**Hva passer best for deg?** 🤔
