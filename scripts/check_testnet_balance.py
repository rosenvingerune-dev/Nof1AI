"""
Check Hyperliquid Testnet Balance
Verifiserer at wallet har mottatt testnet tokens.
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.backend.config_loader import CONFIG


async def check_balance():
    """Sjekk testnet balance."""
    print("\n" + "=" * 70)
    print("HYPERLIQUID TESTNET BALANCE CHECK")
    print("=" * 70)

    # Check configuration
    print("\n📋 Checking configuration...")

    network = CONFIG.get("hyperliquid_network", "mainnet")
    private_key = CONFIG.get("hyperliquid_private_key")
    mnemonic = CONFIG.get("mnemonic")

    print(f"✓ Network: {network}")

    if network != "testnet":
        print("\n⚠️  WARNING: Not configured for testnet!")
        print(f"   Current network: {network}")
        print("\n   Set in .env:")
        print("   HYPERLIQUID_NETWORK=testnet")
        return False

    if not private_key and not mnemonic:
        print("\n❌ No wallet credentials found!")
        print("\n   Set in .env:")
        print("   HYPERLIQUID_PRIVATE_KEY=0x...")
        print("   OR")
        print("   MNEMONIC=your twelve words here")
        return False

    # Initialize API
    print("\n🔌 Connecting to Hyperliquid testnet...")

    try:
        from src.backend.trading.hyperliquid_api import HyperliquidAPI

        api = HyperliquidAPI()
        print(f"✓ Connected to: {api.base_url}")
        print(f"✓ Wallet address: {api.wallet.address}")

    except Exception as e:
        print(f"\n❌ Failed to initialize API: {e}")
        print("\n   Possible causes:")
        print("   1. Invalid private key format")
        print("   2. Invalid mnemonic phrase")
        print("   3. Network connection issue")
        return False

    # Fetch balance
    print("\n💰 Fetching account balance...")

    try:
        state = await api.get_user_state()

        balance = state.get("balance", 0)
        total_value = state.get("total_value", 0)
        positions = state.get("positions", [])

        print("\n" + "=" * 70)
        print("ACCOUNT STATE")
        print("=" * 70)

        print(f"\n💵 Balance: ${balance:,.2f} USDC")
        print(f"💎 Total Value: ${total_value:,.2f}")
        print(f"📊 Open Positions: {len(positions)}")

        if len(positions) > 0:
            print("\n📈 Current Positions:")
            for pos in positions:
                coin = pos.get("coin", "?")
                size = float(pos.get("szi", 0))
                entry_px = float(pos.get("entryPx", 0))
                pnl = pos.get("pnl", 0)
                side = "LONG" if size > 0 else "SHORT"

                print(f"\n   {coin}:")
                print(f"      Side: {side}")
                print(f"      Size: {abs(size):.4f}")
                print(f"      Entry: ${entry_px:,.2f}")
                print(f"      PnL: ${pnl:+,.2f}")

        # Verdict
        print("\n" + "=" * 70)
        print("STATUS")
        print("=" * 70)

        if balance == 0 and total_value == 0:
            print("\n❌ No testnet funds found!")
            print("\n   You need to get testnet tokens from Discord faucet:")
            print("\n   1. Join: https://discord.gg/hyperliquid")
            print("   2. Go to #testnet-faucet channel")
            print(f"   3. Send: !faucet {api.wallet.address}")
            print("   4. Wait 10-30 seconds")
            print("   5. Run this script again to verify")
            return False

        elif balance > 0:
            print("\n✅ Testnet wallet is funded!")
            print(f"\n   Balance: ${balance:,.2f} USDC")
            print("   You can now start trading on testnet!")
            print("\n   Next steps:")
            print("   1. Run: python tests/test_03_hyperliquid_api.py")
            print("   2. Run: python tests/test_all.py")
            print("   3. Start bot: python main.py")
            return True

        else:
            print("\n⚠️  Unexpected account state")
            print(f"   Balance: ${balance:,.2f}")
            print(f"   Total Value: ${total_value:,.2f}")
            return False

    except Exception as e:
        print(f"\n❌ Failed to fetch balance: {e}")
        print("\n   Possible causes:")
        print("   1. Network connection issue")
        print("   2. Hyperliquid testnet is down")
        print("   3. Invalid wallet configuration")
        print("\n   Check status: https://status.hyperliquid.xyz")
        return False


async def check_market_data():
    """Vis eksempel markedsdata fra testnet."""
    print("\n" + "=" * 70)
    print("MARKET DATA CHECK")
    print("=" * 70)

    try:
        from src.backend.trading.hyperliquid_api import HyperliquidAPI

        api = HyperliquidAPI()

        print("\n📊 Fetching market data for BTC and ETH...")

        assets = ["BTC", "ETH"]

        for asset in assets:
            try:
                price = await api.get_current_price(asset)
                funding = await api.get_funding_rate(asset)
                oi = await api.get_open_interest(asset)

                print(f"\n{asset}:")
                print(f"   Price: ${price:,.2f}")

                if funding is not None:
                    funding_pct = funding * 100
                    print(f"   Funding: {funding_pct:+.4f}% per 8h")

                if oi is not None:
                    print(f"   Open Interest: {oi:,.0f} contracts")

            except Exception as e:
                print(f"\n⚠️  Failed to fetch data for {asset}: {e}")

        print("\n✓ Market data is accessible")
        return True

    except Exception as e:
        print(f"\n❌ Failed to fetch market data: {e}")
        return False


async def main():
    """Main check flow."""
    print("\n" + "🔍" * 35)
    print("Hyperliquid Testnet Balance Checker")
    print("🔍" * 35)

    # Check balance
    balance_ok = await check_balance()

    if balance_ok:
        # If balance OK, also check market data
        await check_market_data()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if balance_ok:
        print("\n✅ All checks passed!")
        print("\n   Your testnet setup is ready for trading.")
        print("\n   Recommended next steps:")
        print("   1. Run full test suite: python tests/test_all.py")
        print("   2. Start the trading bot: python main.py")
        print("   3. Use MANUAL mode first to review AI decisions")
    else:
        print("\n⚠️  Setup incomplete")
        print("\n   Follow the instructions above to fix the issues.")
        print("\n   If you need to generate a new wallet:")
        print("   python scripts/setup_hyperliquid_testnet.py")

    print("\n" + "=" * 70 + "\n")

    return balance_ok


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
