"""
Check if wallet is activated on Hyperliquid mainnet
Verifiserer om du kan bruke testnet faucet.
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.backend.config_loader import CONFIG


async def check_mainnet_activity():
    """Sjekk om wallet har vært aktiv på mainnet."""
    print("\n" + "=" * 70)
    print("HYPERLIQUID WALLET ACTIVATION CHECK")
    print("=" * 70)

    print("\n📋 Checking wallet configuration...")

    private_key = CONFIG.get("hyperliquid_private_key")
    mnemonic = CONFIG.get("mnemonic")

    if not private_key and not mnemonic:
        print("\n❌ No wallet credentials found!")
        print("   Set HYPERLIQUID_PRIVATE_KEY or MNEMONIC in .env")
        return False

    # Initialize API with MAINNET
    print("\n🔌 Connecting to Hyperliquid MAINNET...")
    print("   (Don't worry - we're just checking, not trading)")

    try:
        # Temporarily override network to check mainnet
        import os
        original_network = os.environ.get("HYPERLIQUID_NETWORK")
        os.environ["HYPERLIQUID_NETWORK"] = "mainnet"

        from src.backend.trading.hyperliquid_api import HyperliquidAPI

        api = HyperliquidAPI()
        print(f"✓ Wallet address: {api.wallet.address}")

        # Check if wallet has any activity on mainnet
        print("\n🔍 Checking mainnet activity...")

        state = await api.get_user_state()
        balance = state.get("balance", 0)
        total_value = state.get("total_value", 0)
        positions = state.get("positions", [])

        # Restore original network setting
        if original_network:
            os.environ["HYPERLIQUID_NETWORK"] = original_network
        else:
            del os.environ["HYPERLIQUID_NETWORK"]

        print("\n" + "=" * 70)
        print("MAINNET ACTIVITY CHECK")
        print("=" * 70)

        if balance > 0 or total_value > 0 or len(positions) > 0:
            print("\n✅ WALLET IS ACTIVATED!")
            print(f"\n   Mainnet Balance: ${balance:,.2f}")
            print(f"   Mainnet Total Value: ${total_value:,.2f}")
            print(f"   Open Positions: {len(positions)}")

            print("\n✅ You can use Hyperliquid testnet faucet!")
            print("\n   Next steps:")
            print("   1. Go to: https://app.hyperliquid-testnet.xyz")
            print("   2. Connect this wallet")
            print("   3. Click 'Faucet' or 'Get Testnet Tokens'")
            print("   4. Claim 10,000 USDC testnet tokens")
            print("   5. Run: python scripts/check_testnet_balance.py")

            return True

        else:
            print("\n❌ WALLET NOT ACTIVATED")
            print("\n   This wallet has NO activity on Hyperliquid mainnet.")
            print("   Hyperliquid testnet faucet requires mainnet activity.")

            print("\n   Error you'll see on Discord faucet:")
            print("   'Cannot claim drip because user does not exist on mainnet'")

            print("\n" + "=" * 70)
            print("SOLUTIONS")
            print("=" * 70)

            print("\n🎯 Option 1: Use existing wallet (Fastest)")
            print("   If you have MetaMask and have used Hyperliquid before:")
            print("   1. Get private key from MetaMask")
            print("   2. Put it in .env: HYPERLIQUID_PRIVATE_KEY=0x...")
            print("   3. Run this script again")
            print("   4. If activated, use testnet faucet")

            print("\n🎯 Option 2: Activate this wallet (~$5-10)")
            print("   1. Send $5-10 USDC to this wallet on Arbitrum")
            print(f"      Address: {api.wallet.address}")
            print("   2. Go to: https://app.hyperliquid.xyz (MAINNET)")
            print("   3. Connect wallet and deposit USDC")
            print("   4. Make one small trade ($1 worth)")
            print("   5. Now wallet is activated")
            print("   6. Use testnet faucet")

            print("\n🎯 Option 3: Paper trading (100% free)")
            print("   Use simulated exchange (no real API needed)")
            print("   Ask Claude to help build paper trading API")

            print("\n📚 Read more: HYPERLIQUID_TESTNET_WORKAROUND.md")

            return False

    except Exception as e:
        print(f"\n❌ Failed to check mainnet: {e}")
        print("\n   Possible causes:")
        print("   1. Network connection issue")
        print("   2. Invalid private key")
        print("   3. Hyperliquid API is down")
        return False


async def main():
    """Main check flow."""
    print("\n" + "🔍" * 35)
    print("Hyperliquid Wallet Activation Checker")
    print("🔍" * 35)

    print("\nThis script checks if your wallet can use testnet faucet.")
    print("It will connect to MAINNET (read-only) to check activity.")

    activated = await check_mainnet_activity()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if activated:
        print("\n✅ Your wallet can use testnet faucet!")
        print("\n   Claim tokens at: https://app.hyperliquid-testnet.xyz")
    else:
        print("\n❌ Your wallet cannot use testnet faucet yet")
        print("\n   Choose one of the solutions above")
        print("   Read: HYPERLIQUID_TESTNET_WORKAROUND.md")

    print("\n" + "=" * 70 + "\n")

    return activated


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
