"""
Test 1: Environment Configuration
Verifiserer at .env er riktig konfigurert og alle nødvendige variabler er satt.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.backend.config_loader import CONFIG


def test_env_loaded():
    """Test at .env fil er lastet."""
    print("\n" + "=" * 60)
    print("TEST 1: Environment Configuration")
    print("=" * 60)

    # Check LLM provider
    provider = CONFIG.get("llm_provider")
    print(f"\n✓ LLM Provider: {provider}")

    if provider not in ["openrouter", "gemini"]:
        print(f"⚠️  WARNING: LLM_PROVIDER må være 'openrouter' eller 'gemini', fikk: {provider}")
        return False

    return True


def test_gemini_config():
    """Test Gemini-spesifikk konfigurasjon."""
    provider = CONFIG.get("llm_provider")

    if provider == "gemini":
        print("\n--- Gemini Configuration ---")

        api_key = CONFIG.get("gemini_api_key")
        model = CONFIG.get("gemini_model")

        if not api_key:
            print("❌ GEMINI_API_KEY mangler!")
            print("   Få API key fra: https://makersuite.google.com/app/apikey")
            return False

        if api_key.startswith("your_"):
            print("❌ GEMINI_API_KEY er ikke satt (fortsatt placeholder)")
            return False

        print(f"✓ API Key: {api_key[:10]}...{api_key[-4:]} (skjult)")
        print(f"✓ Model: {model}")

        if not model.startswith("gemini"):
            print(f"⚠️  WARNING: GEMINI_MODEL ser ikke ut til å være en gyldig Gemini modell: {model}")

        return True

    return True  # Skip if not using Gemini


def test_openrouter_config():
    """Test OpenRouter-spesifikk konfigurasjon."""
    provider = CONFIG.get("llm_provider")

    if provider == "openrouter":
        print("\n--- OpenRouter Configuration ---")

        api_key = CONFIG.get("openrouter_api_key")
        model = CONFIG.get("llm_model")

        if not api_key:
            print("❌ OPENROUTER_API_KEY mangler!")
            print("   Få API key fra: https://openrouter.ai/keys")
            return False

        print(f"✓ API Key: {api_key[:10]}...{api_key[-4:]} (skjult)")
        print(f"✓ Model: {model}")
        print(f"✓ Base URL: {CONFIG.get('openrouter_base_url')}")

        return True

    return True  # Skip if not using OpenRouter


def test_hyperliquid_config():
    """Test Hyperliquid konfigurasjon."""
    print("\n--- Hyperliquid Configuration ---")

    network = CONFIG.get("hyperliquid_network")
    private_key = CONFIG.get("hyperliquid_private_key")
    mnemonic = CONFIG.get("mnemonic")

    print(f"✓ Network: {network}")

    if network == "mainnet":
        print("⚠️  WARNING: Du bruker MAINNET (ekte penger!)")
        print("   Anbefaler å starte med TESTNET for læring")
    else:
        print("✓ Using TESTNET (safe for learning)")

    if not private_key and not mnemonic:
        print("❌ Ingen wallet credentials!")
        print("   Sett enten HYPERLIQUID_PRIVATE_KEY eller MNEMONIC")
        return False

    if private_key:
        if private_key.startswith("your_"):
            print("❌ HYPERLIQUID_PRIVATE_KEY er placeholder - sett ekte key!")
            return False
        print(f"✓ Private Key: {private_key[:6]}...{private_key[-4:]} (skjult)")

    if mnemonic:
        word_count = len(mnemonic.split())
        print(f"✓ Mnemonic: {word_count} words")

    return True


def test_trading_config():
    """Test trading-spesifikk konfigurasjon."""
    print("\n--- Trading Configuration ---")

    assets = CONFIG.get("assets")
    interval = CONFIG.get("interval")
    trading_mode = CONFIG.get("trading_mode")

    if not assets:
        print("❌ ASSETS mangler!")
        print("   Eksempel: ASSETS=BTC,ETH")
        return False

    print(f"✓ Assets: {assets}")

    if not interval:
        print("❌ INTERVAL mangler!")
        print("   Eksempel: INTERVAL=5m")
        return False

    print(f"✓ Interval: {interval}")
    print(f"✓ Trading Mode: {trading_mode}")

    if trading_mode == "auto":
        print("⚠️  WARNING: AUTO mode er aktivert!")
        print("   Trades vil bli eksekvertert automatisk uten godkjenning")
        print("   Anbefaler MANUAL mode for læring")
    else:
        print("✓ MANUAL mode aktivert - trades krever godkjenning")

    return True


def test_optional_config():
    """Test valgfrie konfigurasjoner."""
    print("\n--- Optional Configuration ---")

    taapi_key = CONFIG.get("taapi_api_key")

    if taapi_key and not taapi_key.startswith("your_"):
        print(f"✓ TAAPI API Key: {taapi_key[:10]}... (satt)")
    else:
        print("⚠️  TAAPI_API_KEY ikke satt (valgfri)")
        print("   Bot kan fortsatt fungere uten TAAPI")
        print("   Få gratis key fra: https://taapi.io")

    return True


def run_all_tests():
    """Kjør alle environment tester."""
    print("\n🔍 Verifiserer environment konfigurasjon...")

    tests = [
        ("Environment loaded", test_env_loaded),
        ("Gemini configuration", test_gemini_config),
        ("OpenRouter configuration", test_openrouter_config),
        ("Hyperliquid configuration", test_hyperliquid_config),
        ("Trading configuration", test_trading_config),
        ("Optional configuration", test_optional_config),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {e}")
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
        print("\n🎉 All tests passed! Configuration looks good.")
        print("\nNext step: Run test_02_gemini_api.py")
        return True
    else:
        print("\n⚠️  Some tests failed. Fix configuration before proceeding.")
        print("\nTips:")
        print("1. Check .env file exists")
        print("2. Verify all API keys are set")
        print("3. Make sure no placeholder values remain")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
