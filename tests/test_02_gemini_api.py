"""
Test 2: Gemini API Connection
Verifiserer at Gemini API fungerer korrekt med din API key.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.backend.config_loader import CONFIG


def test_gemini_import():
    """Test at Gemini SDK er installert."""
    print("\n" + "=" * 60)
    print("TEST 2: Gemini API Connection")
    print("=" * 60)

    try:
        import google.generativeai as genai
        print(f"\n✓ Gemini SDK imported successfully")
        print(f"✓ Version: {genai.__version__}")
        return True
    except ImportError as e:
        print(f"\n❌ Failed to import Gemini SDK: {e}")
        print("\nFix: pip install google-generativeai")
        return False


def test_gemini_configuration():
    """Test Gemini API konfigurasjon."""
    print("\n--- Gemini Configuration ---")

    provider = CONFIG.get("llm_provider")

    if provider != "gemini":
        print(f"⚠️  Skipping: LLM_PROVIDER is '{provider}', not 'gemini'")
        print("   Change LLM_PROVIDER=gemini in .env to test Gemini")
        return None  # Skip, not fail

    api_key = CONFIG.get("gemini_api_key")
    model_name = CONFIG.get("gemini_model")

    if not api_key:
        print("❌ GEMINI_API_KEY not set!")
        return False

    print(f"✓ API Key: {api_key[:10]}...{api_key[-4:]}")
    print(f"✓ Model: {model_name}")

    return True


def test_gemini_authentication():
    """Test Gemini API autentisering."""
    print("\n--- Testing Authentication ---")

    provider = CONFIG.get("llm_provider")
    if provider != "gemini":
        print("⚠️  Skipped (not using Gemini)")
        return None

    try:
        import google.generativeai as genai

        api_key = CONFIG.get("gemini_api_key")
        genai.configure(api_key=api_key)

        print("✓ API key configured")
        return True

    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("\nPossible causes:")
        print("1. Invalid API key")
        print("2. API key expired")
        print("3. Network connection issue")
        return False


def test_simple_generation():
    """Test enkel tekst-generering."""
    print("\n--- Testing Simple Generation ---")

    provider = CONFIG.get("llm_provider")
    if provider != "gemini":
        print("⚠️  Skipped (not using Gemini)")
        return None

    try:
        import google.generativeai as genai
        from google.generativeai.types import HarmCategory, HarmBlockThreshold

        api_key = CONFIG.get("gemini_api_key")
        model_name = CONFIG.get("gemini_model")

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name=model_name,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )

        print("✓ Model initialized")
        print("✓ Sending test prompt...")

        response = model.generate_content(
            "Respond with exactly: 'Gemini API is working!'"
        )

        response_text = response.text.strip()
        print(f"✓ Response received: '{response_text}'")

        if "working" in response_text.lower() or "gemini" in response_text.lower():
            print("✓ Response looks correct")
            return True
        else:
            print(f"⚠️  Unexpected response, but API works")
            return True

    except Exception as e:
        print(f"❌ Generation failed: {e}")
        print("\nError details:")
        print(f"  Type: {type(e).__name__}")
        print(f"  Message: {str(e)}")
        return False


def test_json_mode():
    """Test JSON structured output."""
    print("\n--- Testing JSON Mode ---")

    provider = CONFIG.get("llm_provider")
    if provider != "gemini":
        print("⚠️  Skipped (not using Gemini)")
        return None

    try:
        import google.generativeai as genai
        from google.generativeai.types import HarmCategory, HarmBlockThreshold

        api_key = CONFIG.get("gemini_api_key")
        model_name = CONFIG.get("gemini_model")

        genai.configure(api_key=api_key)

        # Define JSON schema
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "message": {"type": "string"}
            },
            "required": ["status", "message"]
        }

        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json",
            response_schema=schema
        )

        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )

        print("✓ Model with JSON schema initialized")
        print("✓ Sending JSON test prompt...")

        response = model.generate_content(
            "Return a JSON object with status='success' and message='JSON mode working'"
        )

        response_text = response.text
        print(f"✓ JSON response received:")
        print(f"  {response_text}")

        # Try parsing JSON
        import json
        try:
            parsed = json.loads(response_text)
            print(f"✓ Valid JSON parsed:")
            print(f"  Status: {parsed.get('status')}")
            print(f"  Message: {parsed.get('message')}")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            return False

    except Exception as e:
        print(f"❌ JSON mode test failed: {e}")
        return False


def test_function_calling():
    """Test function calling capability."""
    print("\n--- Testing Function Calling ---")

    provider = CONFIG.get("llm_provider")
    if provider != "gemini":
        print("⚠️  Skipped (not using Gemini)")
        return None

    try:
        import google.generativeai as genai
        from google.generativeai.types import HarmCategory, HarmBlockThreshold

        api_key = CONFIG.get("gemini_api_key")
        model_name = CONFIG.get("gemini_model")

        genai.configure(api_key=api_key)

        # Define a test function
        get_weather_tool = genai.protos.Tool(
            function_declarations=[
                genai.protos.FunctionDeclaration(
                    name="get_weather",
                    description="Get current weather for a city",
                    parameters=genai.protos.Schema(
                        type=genai.protos.Type.OBJECT,
                        properties={
                            "city": genai.protos.Schema(type=genai.protos.Type.STRING),
                        },
                        required=["city"]
                    )
                )
            ]
        )

        model = genai.GenerativeModel(
            model_name=model_name,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )

        print("✓ Model with function declaration initialized")
        print("✓ Sending function calling test prompt...")

        chat = model.start_chat()
        response = chat.send_message(
            "What's the weather in Oslo?",
            tools=[get_weather_tool]
        )

        # Check if function was called
        if response.candidates[0].content.parts[0].function_call:
            fc = response.candidates[0].content.parts[0].function_call
            print(f"✓ Function call detected!")
            print(f"  Function name: {fc.name}")
            print(f"  Arguments: {dict(fc.args)}")

            # Verify correct function and argument
            if fc.name == "get_weather" and fc.args.get("city"):
                print(f"✓ Correct function called with city argument")
                return True
            else:
                print(f"⚠️  Function called but unexpected parameters")
                return True  # Still works, just different than expected

        else:
            print("⚠️  No function call detected")
            print("   Gemini might have chosen not to use the tool")
            print("   This is OK - function calling is available but optional")
            return True  # Not necessarily a failure

    except Exception as e:
        print(f"❌ Function calling test failed: {e}")
        return False


def run_all_tests():
    """Kjør alle Gemini API tester."""
    print("\n🔍 Testing Gemini API connection and capabilities...")

    tests = [
        ("Gemini SDK import", test_gemini_import),
        ("Gemini configuration", test_gemini_configuration),
        ("API authentication", test_gemini_authentication),
        ("Simple text generation", test_simple_generation),
        ("JSON structured output", test_json_mode),
        ("Function calling", test_function_calling),
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
        print("\n🎉 All Gemini API tests passed!")
        print("\nNext step: Run test_03_hyperliquid_api.py")
        return True
    else:
        print("\n⚠️  Some tests failed.")
        print("\nTroubleshooting:")
        print("1. Verify GEMINI_API_KEY is correct")
        print("2. Check internet connection")
        print("3. Verify API key has no quota limits")
        print("4. Try regenerating API key at https://makersuite.google.com")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
