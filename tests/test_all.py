"""
Master Test Suite - Kjører alle tester i riktig rekkefølge
"""

import sys
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Determine trading backend
trading_backend = os.getenv("TRADING_BACKEND", "hyperliquid").lower()

# Test sequence based on backend
if trading_backend == "paper":
    TESTS = [
        ("01_environment", "Environment Configuration"),
        ("02_gemini_api", "Gemini API Connection"),
        ("05_paper_trading", "Paper Trading API"),
        ("04_gemini_trading_agent", "Gemini Trading Agent"),
    ]
    print(f"\n🔍 Detected TRADING_BACKEND=paper - Using paper trading test suite")
else:
    TESTS = [
        ("01_environment", "Environment Configuration"),
        ("02_gemini_api", "Gemini API Connection"),
        ("03_hyperliquid_api", "Hyperliquid API Connection"),
        ("04_gemini_trading_agent", "Gemini Trading Agent"),
    ]
    print(f"\n🔍 Detected TRADING_BACKEND={trading_backend} - Using Hyperliquid test suite")


def run_test(test_name, description):
    """Kjør en enkelt test og returner resultat."""
    print("\n" + "=" * 70)
    print(f"Running: {description}")
    print("=" * 70)

    test_file = Path(__file__).parent / f"test_{test_name}.py"

    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False

    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=False,
            text=True
        )

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Failed to run test: {e}")
        return False


def main():
    """Kjør alle tester i sekvens."""
    print("\n" + "🚀" * 35)
    print("nof1.ai Gemini Integration - Complete Test Suite")
    print("🚀" * 35)

    results = {}

    for test_name, description in TESTS:
        success = run_test(test_name, description)
        results[description] = success

        if not success:
            print(f"\n⚠️  Test '{description}' failed!")
            print("Fix this test before proceeding to the next one.")

            user_input = input("\nContinue anyway? (y/N): ").strip().lower()
            if user_input != 'y':
                print("\nStopping test suite.")
                break

    # Final summary
    print("\n" + "=" * 70)
    print("COMPLETE TEST SUITE SUMMARY")
    print("=" * 70)

    passed = sum(1 for success in results.values() if success)
    total = len(results)

    for description, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {description}")

    print(f"\nTotal: {passed}/{total} test suites passed")

    # Final verdict
    if passed == total:
        print("\n" + "🎉" * 35)
        print("ALL TESTS PASSED!")
        print("🎉" * 35)
        print("\nYour nof1.ai setup with Gemini is fully configured!")
        print("\n✅ Next steps:")
        print("   1. Review GEMINI_SETUP.md for usage instructions")
        print("   2. Start the bot: python main.py")
        print("   3. Test in MANUAL mode first")
        print("   4. Monitor trades in the GUI\n")
        return True
    else:
        print("\n" + "⚠️ " * 35)
        print(f"Some tests failed ({total - passed} failures)")
        print("⚠️ " * 35)
        print("\n🔧 Troubleshooting:")
        print("   1. Check .env file has all required keys")
        print("   2. Verify API keys are valid")
        print("   3. Run individual tests for detailed error messages:")
        print("      python tests/test_01_environment.py")
        print("      python tests/test_02_gemini_api.py")

        if trading_backend == "paper":
            print("      python tests/test_05_paper_trading.py")
        else:
            print("      python tests/test_03_hyperliquid_api.py")

        print("      python tests/test_04_gemini_trading_agent.py")
        print("\n   4. Check log files:")
        print("      - bot.log")
        print("      - llm_requests.log")

        if trading_backend == "paper":
            print("\n   5. Paper Trading Resources:")
            print("      - Read: PAPER_TRADING_GUIDE.md")
            print("      - Verify: Internet connection (needs Binance API)")
        else:
            print("\n   5. Hyperliquid Resources:")
            print("      - Read: HYPERLIQUID_TESTNET_WORKAROUND.md")
            print("      - Check: Wallet activation status")

        print()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
