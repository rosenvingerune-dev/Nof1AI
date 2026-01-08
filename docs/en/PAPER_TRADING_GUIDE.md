# 📄 Paper Trading Guide

This guide explains how to use the **Paper Trading** mode in Nof1.ai trading bot.
Paper trading allows you to test strategies and the bot's functionality **without risking real money**.

## 🚀 How it Works

The Paper Trading backend replaces the real Hyperliquid exchange connection with a local simulation.
- **Prices**: Fetched in real-time from Binance (via public API).
- **Orders**: Simulated locally (Limit, Market, TP/SL).
- **Balance**: Starts with a simulated $10,000 USDC.
- **Positions**: Tracked locally in `data/paper_trading_state.json`.

---

## 🛠️ Setup

1. **Configure `.env`**:
   Ensure your `.env` file has the following setting:
   ```properties
   TRADING_BACKEND=paper
   ```

2. **No API Keys Needed**: 
   Since it's simulated, you don't need Hyperliquid keys. The bot just needs internet access to fetch prices.

---

## ▶️ Running the Bot

### **Method 1: Using the Startup Script (Recommended)**
Double-click or run the `start_all.ps1` script in the root folder.
```powershell
.\start_all.ps1
```
This will launch both the Backend (FastAPI) and the Frontend (React).

### **Method 2: Manual Start**

**Backend:**
```powershell
# Open terminal 1
python -m uvicorn src.api.main:app --reload
```

**Frontend:**
```powershell
# Open terminal 2
cd frontend
npm run dev
```

---

## 🖥️ Using the Interface

1. Open **http://localhost:5173** in your browser.
2. Go to the **Dashboard**.
3. You should see a balance of **$10,000**.
4. You can click "Start Bot" to enable auto-trading (if configured) or trade manually via the interface.

---

## 🧪 reset Simulation

To reset your balance and positions:
1. Stop the bot.
2. Delete the state file:
   ```
   data/paper_trading_state.json
   ```
3. Restart the bot. Your balance will reset to $10,000.

---

## 📝 Troubleshooting

- **Prices are 0**: Check your internet connection. The bot needs to reach Binance API.
- **Orders not filling**: Limit orders only fill if the real-world price crosses your limit price.
- **"Backend not connected"**: Ensure the Python backend is running.
