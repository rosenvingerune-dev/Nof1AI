"""
Test 3: Hyperliquid API Connection
Verifiserer at Hyperliquid exchange API fungerer korrekt.
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.backend.config_loader import CONFIG


def test_hyperliquid_import():
    """Test at Hyperliquid SDK er installert."""
    print("\n" + "=" * 60)
    print("TEST 3: Hyperliquid API Connection")
    print("=" * 60)

    try:
        from src.backend.trading.hyperliquid_api import HyperliquidAPI
        print(f"\n✓ HyperliquidAPI imported successfully")
        return True
    except ImportError as e:
        print(f"\n❌ Failed to import HyperliquidAPI: {e}")
        print("\nFix: pip install hyperliquid-python-sdk")
        return False


async def test_api_initialization():
    """Test Hyperliquid API initialisering."""
    print("\n--- Testing API Initialization ---")

    try:
        from src.backend.trading.hyperliquid_api import HyperliquidAPI

        api = HyperliquidAPI()
        print("✓ HyperliquidAPI initialized")

        network = CONFIG.get("hyperliquid_network", "mainnet")
        print(f"✓ Network: {network}")

        if network == "mainnet":
            print("⚠️  WARNING: Connected to MAINNET (real money!)")
        else:
            print("✓ Connected to TESTNET (safe)")

        print(f"✓ Wallet address: {api.wallet.address}")

        return True

    except ValueError as e:
        print(f"❌ Initialization failed: {e}")
        print("\nPossible causes:")
        print("1. Missing HYPERLIQUID_PRIVATE_KEY or MNEMONIC")
        print("2. Invalid private key format")
        print("3. Invalid mnemonic phrase")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


async def test_get_user_state():
    """Test henting av account state."""
    print("\n--- Testing Get User State ---")

    try:
        from src.backend.trading.hyperliquid_api import HyperliquidAPI

        api = HyperliquidAPI()
        print("✓ Fetching account state...")

        state = await api.get_user_state()

        balance = state.get("balance", 0)
        total_value = state.get("total_value", 0)
        positions = state.get("positions", [])

        print(f"✓ Balance: ${balance:,.2f} USDC")
        print(f"✓ Total Value: ${total_value:,.2f}")
        print(f"✓ Open Positions: {len(positions)}")

        if len(positions) > 0:
            print("\n  Current Positions:")
            for pos in positions:
                coin = pos.get("coin", "?")
                size = float(pos.get("szi", 0))
                entry_px = float(pos.get("entryPx", 0))
                pnl = pos.get("pnl", 0)
                side = "LONG" if size > 0 else "SHORT"

                print(f"    {coin}: {side} {abs(size):.4f} @ ${entry_px:,.2f} | PnL: ${pnl:+,.2f}")

        if balance == 0 and total_value == 0:
            network = CONFIG.get("hyperliquid_network", "mainnet")
            if network == "testnet":
                print("\n⚠️  WARNING: Testnet balance is 0!")
                print("   Get testnet tokens from Hyperliquid Discord:")
                print("   1. Join: https://discord.gg/hyperliquid")
                print("   2. Go to #testnet-faucet")
                print(f"   3. Send: !faucet {api.wallet.address}")
                return False

        return True

    except Exception as e:
        print(f"❌ Failed to get user state: {e}")
        print("\nPossible causes:")
        print("1. Network connection issue")
        print("2. Hyperliquid API is down")
        print("3. Invalid wallet credentials")
        return False


async def test_get_current_price():
    """Test henting av sanntidspriser."""
    print("\n--- Testing Get Current Price ---")

    try:
        from src.backend.trading.hyperliquid_api import HyperliquidAPI

        api = HyperliquidAPI()

        assets_to_test = ["BTC", "ETH"]

        print("✓ Fetching current prices...")

        for asset in assets_to_test:
            price = await api.get_current_price(asset)

            if price > 0:
                print(f"✓ {asset}: ${price:,.2f}")
            else:
                print(f"⚠️  {asset}: Price is 0 or unavailable")

        return True

    except Exception as e:
        print(f"❌ Failed to get prices: {e}")
        return False


async def test_get_funding_rate():
    """Test henting av funding rates."""
    print("\n--- Testing Get Funding Rate ---")

    try:
        from src.backend.trading.hyperliquid_api import HyperliquidAPI

        api = HyperliquidAPI()

        assets_to_test = ["BTC", "ETH"]

        print("✓ Fetching funding rates...")

        for asset in assets_to_test:
            funding = await api.get_funding_rate(asset)

            if funding is not None:
                funding_pct = funding * 100
                print(f"✓ {asset}: {funding_pct:+.4f}% per 8h")

                if abs(funding_pct) > 0.1:
                    if funding_pct > 0:
                        print(f"    → Longs betaler shorts (bullish sentiment)")
                    else:
                        print(f"    → Shorts betaler longs (bearish sentiment)")
            else:
                print(f"⚠️  {asset}: Funding rate unavailable")

        return True

    except Exception as e:
        print(f"❌ Failed to get funding rates: {e}")
        return False


async def test_get_open_interest():
    """Test henting av open interest."""
    print("\n--- Testing Get Open Interest ---")

    try:
        from src.backend.trading.hyperliquid_api import HyperliquidAPI

        api = HyperliquidAPI()

        assets_to_test = ["BTC", "ETH"]

        print("✓ Fetching open interest...")

        for asset in assets_to_test:
            oi = await api.get_open_interest(asset)

            if oi is not None:
                print(f"✓ {asset}: {oi:,.0f} contracts")
            else:
                print(f"⚠️  {asset}: Open interest unavailable")

        return True

    except Exception as e:
        print(f"❌ Failed to get open interest: {e}")
        return False


async def test_get_open_orders():
    """Test henting av open orders."""
    print("\n--- Testing Get Open Orders ---")

    try:
        from src.backend.trading.hyperliquid_api import HyperliquidAPI

        api = HyperliquidAPI()
        print("✓ Fetching open orders...")

        orders = await api.get_open_orders()

        print(f"✓ Open Orders: {len(orders)}")

        if len(orders) > 0:
            print("\n  Active Orders:")
            for order in orders[:5]:  # Show max 5
                coin = order.get("coin", "?")
                side = "BUY" if order.get("side") == "B" else "SELL"
                size = order.get("sz", 0)
                limit_px = order.get("limitPx", 0)
                oid = order.get("oid", "?")

                print(f"    {coin}: {side} {size} @ ${limit_px} (ID: {oid})")

        return True

    except Exception as e:
        print(f"❌ Failed to get open orders: {e}")
        return False


async def run_async_tests():
    """Kjør alle async tester."""
    tests = [
        ("API initialization", test_api_initialization),
        ("Get user state", test_get_user_state),
        ("Get current prices", test_get_current_price),
        ("Get funding rates", test_get_funding_rate),
        ("Get open interest", test_get_open_interest),
        ("Get open orders", test_get_open_orders),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    return results


def run_all_tests():
    """Kjør alle Hyperliquid API tester."""
    print("\n🔍 Testing Hyperliquid API connection...")

    # First test import (sync)
    import_ok = test_hyperliquid_import()
    if not import_ok:
        return False

    # Run async tests
    results = asyncio.run(run_async_tests())

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result) + (1 if import_ok else 0)
    total = len(results) + 1

    print(f"✅ PASS: Hyperliquid SDK import")
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All Hyperliquid API tests passed!")
        print("\nNext step: Run test_04_gemini_trading_agent.py")
        return True
    else:
        print("\n⚠️  Some tests failed.")
        print("\nTroubleshooting:")
        print("1. Verify HYPERLIQUID_PRIVATE_KEY or MNEMONIC is correct")
        print("2. Check network connection")
        print("3. Verify you have testnet funds (if using testnet)")
        print("4. Check Hyperliquid status: https://status.hyperliquid.xyz")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
