"""
Test 05: Paper Trading API Verification

Tests the paper trading backend to ensure it works correctly
for risk-free testing without a real exchange.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def print_header(text: str):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


async def test_paper_trading():
    """Test paper trading API functionality"""

    print_header("TEST 05: PAPER TRADING API")
    print("\nThis test verifies the paper trading backend for risk-free testing.")
    print("No exchange account needed - all trades are simulated locally!")

    # Test 1: Import and Initialize
    print("\n📦 Test 1/8: Importing paper trading API...")
    try:
        from src.backend.trading.paper_trading_api import PaperTradingAPI
        print("✅ Paper trading API imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import paper trading API: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

    # Test 2: Create instance
    print("\n💼 Test 2/8: Creating paper trading instance...")
    try:
        starting_balance = 10000.0
        api = PaperTradingAPI(starting_balance=starting_balance)
        print(f"✅ Paper trading API initialized")
        print(f"   Starting balance: ${api.balance:,.2f} USDC")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return False

    # Test 3: Get user state
    print("\n👤 Test 3/8: Getting user state...")
    try:
        state = await api.get_user_state()
        print(f"✅ User state retrieved")
        print(f"   Balance: ${state['balance']:,.2f} USDC")
        print(f"   Total Value: ${state['total_value']:,.2f}")
        print(f"   Positions: {len(state['positions'])}")

        if state['balance'] != starting_balance:
            print(f"❌ Balance mismatch: expected ${starting_balance}, got ${state['balance']}")
            return False
    except Exception as e:
        print(f"❌ Failed to get user state: {e}")
        return False

    # Test 4: Fetch current price
    print("\n💰 Test 4/8: Fetching current prices...")
    try:
        btc_price = await api.get_current_price("BTC")
        eth_price = await api.get_current_price("ETH")

        print(f"✅ Prices fetched from Binance:")
        print(f"   BTC: ${btc_price:,.2f}")
        print(f"   ETH: ${eth_price:,.2f}")

        if btc_price <= 0 or eth_price <= 0:
            print(f"❌ Invalid prices: BTC={btc_price}, ETH={eth_price}")
            return False
    except Exception as e:
        print(f"❌ Failed to fetch prices: {e}")
        return False

    # Test 5: Place buy order
    print("\n📈 Test 5/8: Placing buy order (simulated)...")
    try:
        asset = "BTC"
        amount = 0.1  # 0.1 BTC

        initial_balance = api.balance
        result = await api.place_buy_order(asset, amount)

        print(f"✅ Buy order executed (simulated)")
        print(f"   Asset: {asset}")
        print(f"   Amount: {amount}")
        print(f"   Result: {result}")

        # Verify balance decreased
        new_balance = api.balance
        cost = amount * btc_price * (1 + api.slippage)
        expected_balance = initial_balance - cost

        print(f"   Balance: ${initial_balance:,.2f} → ${new_balance:,.2f}")
        print(f"   Cost: ${cost:,.2f} (incl. slippage)")

        # Allow small floating point difference
        if abs(new_balance - expected_balance) > 0.01:
            print(f"❌ Balance mismatch: expected ${expected_balance:,.2f}, got ${new_balance:,.2f}")
            return False
    except Exception as e:
        print(f"❌ Failed to place buy order: {e}")
        return False

    # Test 6: Verify position created
    print("\n📊 Test 6/8: Verifying position...")
    try:
        state = await api.get_user_state()
        positions = state['positions']

        if len(positions) != 1:
            print(f"❌ Expected 1 position, found {len(positions)}")
            return False

        pos = positions[0]
        print(f"✅ Position created:")
        print(f"   Asset: {pos['coin']}")
        print(f"   Size: {pos['szi']}")
        print(f"   Entry Price: ${pos['entryPx']:,.2f}")
        print(f"   Current Price: ${btc_price:,.2f}")
        print(f"   PnL: ${pos['pnl']:,.2f}")

        if pos['coin'] != asset:
            print(f"❌ Asset mismatch: expected {asset}, got {pos['coin']}")
            return False

        if abs(float(pos['szi']) - amount) > 0.0001:
            print(f"❌ Size mismatch: expected {amount}, got {pos['szi']}")
            return False
    except Exception as e:
        print(f"❌ Failed to verify position: {e}")
        return False

    # Test 7: Place take profit order
    print("\n🎯 Test 7/8: Placing take profit order...")
    try:
        tp_price = btc_price * 1.1  # 10% above entry
        is_long = True

        result = await api.place_take_profit(asset, is_long, amount, tp_price)

        print(f"✅ Take profit order placed (simulated)")
        print(f"   Asset: {asset}")
        print(f"   TP Price: ${tp_price:,.2f}")
        print(f"   Result: {result}")

        # Verify order exists
        orders = await api.get_open_orders()
        tp_orders = [o for o in orders if o.get('coin') == asset and o.get('order_type') == 'trigger']

        if len(tp_orders) != 1:
            print(f"❌ Expected 1 TP order, found {len(tp_orders)}")
            return False

        print(f"   Order ID: {tp_orders[0]['oid']}")
    except Exception as e:
        print(f"❌ Failed to place TP order: {e}")
        return False

    # Test 8: Place stop loss order
    print("\n🛑 Test 8/8: Placing stop loss order...")
    try:
        sl_price = btc_price * 0.95  # 5% below entry

        result = await api.place_stop_loss(asset, is_long, amount, sl_price)

        print(f"✅ Stop loss order placed (simulated)")
        print(f"   Asset: {asset}")
        print(f"   SL Price: ${sl_price:,.2f}")
        print(f"   Result: {result}")

        # Verify order exists
        orders = await api.get_open_orders()
        trigger_orders = [o for o in orders if o.get('coin') == asset and o.get('order_type') == 'trigger']

        if len(trigger_orders) != 2:  # TP + SL
            print(f"❌ Expected 2 trigger orders (TP+SL), found {len(trigger_orders)}")
            return False

        print(f"   Total trigger orders: {len(trigger_orders)}")
    except Exception as e:
        print(f"❌ Failed to place SL order: {e}")
        return False

    # Summary
    print_header("TEST RESULTS")
    print("\n✅ ALL PAPER TRADING TESTS PASSED!")
    print("\n📋 Summary:")
    print(f"   • Paper trading API initialized successfully")
    print(f"   • Real-time price fetching works (Binance)")
    print(f"   • Market orders execute correctly")
    print(f"   • Position tracking is accurate")
    print(f"   • TP/SL orders work as expected")

    print("\n" + "=" * 70)
    print("WHAT THIS MEANS")
    print("=" * 70)
    print("\n✅ You can use paper trading for risk-free testing!")
    print("\n📝 To use paper trading:")
    print("   1. Set TRADING_BACKEND=paper in .env")
    print("   2. No exchange account needed")
    print("   3. No wallet setup required")
    print("   4. Start bot: python main.py")

    print("\n📚 Read: PAPER_TRADING_GUIDE.md for complete guide")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("\n1. Run all tests:")
    print("   python tests/test_all.py")
    print("\n2. Start bot with paper trading:")
    print("   python main.py")
    print("\n3. Open GUI:")
    print("   http://localhost:3000")
    print("\n4. When ready, switch to real exchange:")
    print("   TRADING_BACKEND=hyperliquid")

    print("\n" + "=" * 70 + "\n")

    return True


async def main():
    """Main test runner"""
    print("\n" + "🧪" * 35)
    print("Paper Trading API Test Suite")
    print("🧪" * 35)

    print("\nTesting the paper trading backend...")
    print("This requires internet connection (Binance price API)")

    success = await test_paper_trading()

    return success


if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
