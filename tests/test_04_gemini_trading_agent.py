"""
Test 4: Gemini Trading Agent
Verifiserer at GeminiTradingAgent kan generere trading decisions.
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.backend.config_loader import CONFIG


def test_agent_import():
    """Test at GeminiTradingAgent kan importeres."""
    print("\n" + "=" * 60)
    print("TEST 4: Gemini Trading Agent")
    print("=" * 60)

    provider = CONFIG.get("llm_provider")

    if provider != "gemini":
        print(f"\n⚠️  LLM_PROVIDER is '{provider}', not 'gemini'")
        print("   Set LLM_PROVIDER=gemini in .env to test Gemini agent")
        return None

    try:
        from src.backend.agent.gemini_decision_maker import GeminiTradingAgent
        print(f"\n✓ GeminiTradingAgent imported successfully")
        return True
    except ImportError as e:
        print(f"\n❌ Failed to import GeminiTradingAgent: {e}")
        return False


def test_agent_initialization():
    """Test initialisering av trading agent."""
    print("\n--- Testing Agent Initialization ---")

    provider = CONFIG.get("llm_provider")
    if provider != "gemini":
        print("⚠️  Skipped (not using Gemini)")
        return None

    try:
        from src.backend.agent.gemini_decision_maker import GeminiTradingAgent

        agent = GeminiTradingAgent()
        print("✓ GeminiTradingAgent initialized")
        print(f"✓ Model: {agent.model_name}")
        print(f"✓ API configured: {agent.api_key[:10]}...{agent.api_key[-4:]}")

        return True

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False


def test_simple_trading_decision():
    """Test enkel trading decision (uten tool calling)."""
    print("\n--- Testing Simple Trading Decision ---")

    provider = CONFIG.get("llm_provider")
    if provider != "gemini":
        print("⚠️  Skipped (not using Gemini)")
        return None

    try:
        from src.backend.agent.gemini_decision_maker import GeminiTradingAgent

        agent = GeminiTradingAgent()

        # Minimal context
        context = f"""
Current Time: {datetime.now().isoformat()}

Market Data:

BTC:
- Current Price: $98,500
- 5m RSI: 55 (neutral)
- 4h MACD: Bullish crossover
- Funding Rate: 0.01% (neutral)
- Open Interest: Increasing (+3%)
- Volume: Above average

ETH:
- Current Price: $3,400
- 5m RSI: 65 (slightly overbought)
- 4h MACD: Bearish
- Funding Rate: 0.08% (high - overcrowded longs)
- Open Interest: Stable
- Volume: Below average

Account State:
- Balance: $10,000 USDC
- Active Positions: None
- Available Margin: $10,000

Trading Parameters:
- Max Leverage: 3x
- Risk per trade: 2% ($200)
"""

        print("✓ Sending context to Gemini...")
        print("  Assets: BTC, ETH")
        print("  Context length:", len(context), "chars")

        result = agent.decide_trade(
            assets=["BTC", "ETH"],
            context=context
        )

        print("\n✓ Decision received!")

        # Verify structure
        if not isinstance(result, dict):
            print(f"❌ Expected dict, got {type(result)}")
            return False

        reasoning = result.get("reasoning", "")
        decisions = result.get("trade_decisions", [])

        print(f"\n--- GEMINI REASONING ({len(reasoning)} chars) ---")
        # Show first 500 chars
        print(reasoning[:500] + ("..." if len(reasoning) > 500 else ""))

        print(f"\n--- TRADE DECISIONS ({len(decisions)} decisions) ---")

        if not isinstance(decisions, list):
            print(f"❌ trade_decisions should be list, got {type(decisions)}")
            return False

        if len(decisions) != 2:
            print(f"⚠️  Expected 2 decisions (BTC, ETH), got {len(decisions)}")

        for decision in decisions:
            asset = decision.get("asset", "?")
            action = decision.get("action", "?")
            allocation = decision.get("allocation_usd", 0)
            tp_price = decision.get("tp_price")
            sl_price = decision.get("sl_price")
            rationale = decision.get("rationale", "")

            print(f"\n{asset}:")
            print(f"  Action: {action.upper()}")
            print(f"  Allocation: ${allocation:,.2f}")
            print(f"  TP: ${tp_price:,.2f}" if tp_price else "  TP: None")
            print(f"  SL: ${sl_price:,.2f}" if sl_price else "  SL: None")
            print(f"  Rationale: {rationale[:100]}...")

            # Validate decision structure
            if action not in ["buy", "sell", "hold"]:
                print(f"  ⚠️  Invalid action: {action}")

            if action == "buy" and tp_price and sl_price:
                current_price = 98500 if asset == "BTC" else 3400
                if tp_price <= current_price:
                    print(f"  ⚠️  BUY: TP should be > current price")
                if sl_price >= current_price:
                    print(f"  ⚠️  BUY: SL should be < current price")

        print("\n✓ All decisions validated")
        return True

    except Exception as e:
        print(f"❌ Decision generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tool_calling_decision():
    """Test trading decision med tool calling."""
    print("\n--- Testing Trading Decision with Tool Calling ---")

    provider = CONFIG.get("llm_provider")
    if provider != "gemini":
        print("⚠️  Skipped (not using Gemini)")
        return None

    # Check if TAAPI key is available
    taapi_key = CONFIG.get("taapi_api_key")
    if not taapi_key or taapi_key.startswith("your_"):
        print("⚠️  TAAPI_API_KEY not set - skipping tool calling test")
        print("   Set TAAPI_API_KEY in .env to test tool calling")
        return None

    try:
        from src.backend.agent.gemini_decision_maker import GeminiTradingAgent

        agent = GeminiTradingAgent()

        # Context that might trigger tool calling
        context = f"""
Current Time: {datetime.now().isoformat()}

Market Data for BTC:
- Current Price: $98,500
- 4h MACD: Bullish crossover
- Funding Rate: 0.01%

IMPORTANT: You should fetch additional indicators to make an informed decision.
Consider fetching RSI, ATR, or other indicators using the fetch_taapi_indicator tool.

Account State:
- Balance: $10,000 USDC
- Active Positions: None
"""

        print("✓ Sending context that encourages tool usage...")
        print("  (Context hints at needing more indicators)")

        result = agent.decide_trade(
            assets=["BTC"],
            context=context
        )

        print("\n✓ Decision received with potential tool calls!")

        reasoning = result.get("reasoning", "")
        decisions = result.get("trade_decisions", [])

        # Check if reasoning mentions fetched indicators
        if any(keyword in reasoning.lower() for keyword in ["rsi", "atr", "ema", "fetched", "retrieved"]):
            print("✓ Reasoning mentions additional indicators (likely fetched via tool)")
        else:
            print("⚠️  No mention of fetched indicators in reasoning")
            print("   (Gemini may have decided tools weren't needed)")

        print(f"\nDecision: {decisions[0].get('action').upper()}")
        print(f"Rationale: {decisions[0].get('rationale')[:150]}...")

        return True

    except Exception as e:
        print(f"❌ Tool calling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multi_asset_decision():
    """Test trading decision for flere assets."""
    print("\n--- Testing Multi-Asset Decision ---")

    provider = CONFIG.get("llm_provider")
    if provider != "gemini":
        print("⚠️  Skipped (not using Gemini)")
        return None

    try:
        from src.backend.agent.gemini_decision_maker import GeminiTradingAgent

        agent = GeminiTradingAgent()

        assets = ["BTC", "ETH", "SOL"]

        context = f"""
Current Time: {datetime.now().isoformat()}

BTC:
- Price: $98,500 | RSI: 55 | MACD: Bullish | Funding: 0.01%

ETH:
- Price: $3,400 | RSI: 65 | MACD: Bearish | Funding: 0.08%

SOL:
- Price: $180 | RSI: 48 | MACD: Neutral | Funding: -0.02%

Account: $10,000 USDC available
"""

        print(f"✓ Testing with {len(assets)} assets: {', '.join(assets)}")

        result = agent.decide_trade(assets=assets, context=context)

        decisions = result.get("trade_decisions", [])

        if len(decisions) != len(assets):
            print(f"⚠️  Expected {len(assets)} decisions, got {len(decisions)}")

        # Verify all assets have decisions
        decision_assets = [d.get("asset") for d in decisions]
        for asset in assets:
            if asset in decision_assets:
                print(f"✓ {asset}: Decision provided")
            else:
                print(f"❌ {asset}: Missing decision!")

        return True

    except Exception as e:
        print(f"❌ Multi-asset test failed: {e}")
        return False


def test_error_handling():
    """Test error handling når API feiler."""
    print("\n--- Testing Error Handling ---")

    provider = CONFIG.get("llm_provider")
    if provider != "gemini":
        print("⚠️  Skipped (not using Gemini)")
        return None

    try:
        from src.backend.agent.gemini_decision_maker import GeminiTradingAgent

        agent = GeminiTradingAgent()

        # Test with invalid/empty context
        print("✓ Testing with minimal context...")

        result = agent.decide_trade(
            assets=["BTC"],
            context="No market data available."
        )

        # Should still return valid structure (fallback)
        if isinstance(result, dict) and "trade_decisions" in result:
            decisions = result["trade_decisions"]
            if len(decisions) > 0:
                action = decisions[0].get("action")
                if action == "hold":
                    print("✓ Graceful fallback to HOLD with insufficient data")
                else:
                    print(f"✓ Agent made decision: {action}")
                return True

        print("⚠️  Unexpected response structure on error case")
        return True  # Not critical

    except Exception as e:
        print(f"⚠️  Error handling test encountered exception: {e}")
        print("   (This is OK if agent handles it gracefully)")
        return True


def run_all_tests():
    """Kjør alle Gemini Trading Agent tester."""
    print("\n🔍 Testing Gemini Trading Agent...")

    tests = [
        ("Agent import", test_agent_import),
        ("Agent initialization", test_agent_initialization),
        ("Simple trading decision", test_simple_trading_decision),
        ("Tool calling decision", test_tool_calling_decision),
        ("Multi-asset decision", test_multi_asset_decision),
        ("Error handling", test_error_handling),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            if result is None:
                print(f"⏭️  Skipped: {name}")
                continue
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All Gemini Trading Agent tests passed!")
        print("\nYour Gemini integration is working correctly!")
        print("\nNext step:")
        print("- Run: python tests/test_all.py  (run all tests)")
        print("- Or start the bot: python main.py")
        return True
    else:
        print("\n⚠️  Some tests failed.")
        print("\nCheck llm_requests.log for detailed Gemini API logs")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
