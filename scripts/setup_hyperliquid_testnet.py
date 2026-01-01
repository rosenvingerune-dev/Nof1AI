"""
Hyperliquid Testnet Setup Script
Genererer en ny wallet og viser hvordan du får testnet tokens.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def generate_wallet():
    """Generer en ny Ethereum wallet for Hyperliquid testnet."""
    print("\n" + "=" * 70)
    print("HYPERLIQUID TESTNET WALLET GENERATOR")
    print("=" * 70)

    try:
        from eth_account import Account
    except ImportError:
        print("\n❌ eth_account ikke installert!")
        print("\nInstaller med:")
        print("  pip install web3")
        return None

    # Generate new account
    print("\n🔐 Genererer ny Ethereum wallet...")
    account = Account.create()

    print("\n✅ Wallet generert!")
    print("\n" + "=" * 70)
    print("WALLET INFORMASJON")
    print("=" * 70)
    print(f"\n📍 Address:")
    print(f"   {account.address}")
    print(f"\n🔑 Private Key:")
    print(f"   {account.key.hex()}")
    print("\n" + "=" * 70)

    # Warnings
    print("\n⚠️  VIKTIG SIKKERHETSADVARSLER:")
    print("   1. Dette er en TESTNET wallet - bruk KUN til testing!")
    print("   2. ALDRI bruk denne på mainnet med ekte penger")
    print("   3. ALDRI del private key med andre")
    print("   4. Lagre private key trygt (f.eks. i .env fil)")
    print("   5. Bruk en ANNEN wallet for mainnet trading")

    return {
        "address": account.address,
        "private_key": account.key.hex()
    }


def show_testnet_instructions(wallet_info):
    """Vis instruksjoner for å få testnet tokens."""
    print("\n" + "=" * 70)
    print("HVORDAN FÅ TESTNET TOKENS")
    print("=" * 70)

    print("\n📝 Steg 1: Join Hyperliquid Discord")
    print("   URL: https://discord.gg/hyperliquid")
    print("   - Klikk på linken")
    print("   - Logg inn med Discord-kontoen din")
    print("   - Godta server-reglene")

    print("\n📝 Steg 2: Gå til #testnet-faucet kanal")
    print("   - Finn kanalen i venstre sidebar")
    print("   - Klikk på den")

    print("\n📝 Steg 3: Send faucet kommando")
    print("   Kopier og lim inn denne kommandoen i kanalen:")
    print("\n   " + "─" * 66)
    if wallet_info:
        print(f"   !faucet {wallet_info['address']}")
    else:
        print("   !faucet YOUR_WALLET_ADDRESS")
    print("   " + "─" * 66)

    print("\n📝 Steg 4: Vent på tokens")
    print("   - Bot svarer innen 10-30 sekunder")
    print("   - Du mottar 10,000 USDC testnet tokens")
    print("   - Kan gjøres én gang per wallet")

    print("\n📝 Steg 5: Verifiser at du fikk tokens")
    print("   Kjør denne kommandoen:")
    print("\n   python scripts/check_testnet_balance.py")


def show_env_configuration(wallet_info):
    """Vis hvordan man legger til wallet i .env."""
    print("\n" + "=" * 70)
    print("KONFIGURASJON AV .ENV FIL")
    print("=" * 70)

    print("\n📝 Legg til følgende i .env filen:")
    print("\n   " + "─" * 66)
    print("   # Hyperliquid Testnet Configuration")
    print("   HYPERLIQUID_NETWORK=testnet")
    if wallet_info:
        print(f"   HYPERLIQUID_PRIVATE_KEY={wallet_info['private_key']}")
    else:
        print("   HYPERLIQUID_PRIVATE_KEY=your_private_key_here")
    print("   " + "─" * 66)

    print("\n⚠️  HUSK:")
    print("   - ALDRI commit .env til git!")
    print("   - .env er allerede i .gitignore")
    print("   - Private key MÅ starte med '0x'")


def save_wallet_to_file(wallet_info):
    """Tilbyr å lagre wallet info til fil."""
    print("\n" + "=" * 70)
    print("LAGRE WALLET INFORMASJON")
    print("=" * 70)

    response = input("\nVil du lagre wallet-informasjonen til en fil? (y/N): ").strip().lower()

    if response == 'y':
        filename = "testnet_wallet.txt"
        filepath = Path(__file__).parent.parent / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("HYPERLIQUID TESTNET WALLET\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Address: {wallet_info['address']}\n")
            f.write(f"Private Key: {wallet_info['private_key']}\n\n")
            f.write("=" * 70 + "\n")
            f.write("SECURITY WARNINGS:\n")
            f.write("=" * 70 + "\n")
            f.write("1. This is a TESTNET wallet - use ONLY for testing!\n")
            f.write("2. NEVER use this on mainnet with real money\n")
            f.write("3. NEVER share this private key\n")
            f.write("4. DELETE this file after copying to .env\n")
            f.write("=" * 70 + "\n")

        print(f"\n✅ Wallet informasjon lagret til: {filepath}")
        print("\n⚠️  VIKTIG: Slett denne filen etter du har kopiert til .env!")
        print(f"   Kommando: del {filename}")
    else:
        print("\n✅ Wallet informasjon ikke lagret.")
        print("   Kopier private key manuelt til .env")


def main():
    """Main setup flow."""
    print("\n" + "🚀" * 35)
    print("Hyperliquid Testnet Setup")
    print("🚀" * 35)

    print("\nDenne scriptet vil:")
    print("  1. Generere en ny Ethereum wallet")
    print("  2. Vise deg hvordan du får testnet tokens")
    print("  3. Hjelpe deg med .env konfigurasjon")

    response = input("\nVil du fortsette? (Y/n): ").strip().lower()
    if response == 'n':
        print("\nAvbrutt av bruker.")
        return

    # Generate wallet
    wallet_info = generate_wallet()

    if not wallet_info:
        print("\n❌ Kunne ikke generere wallet. Sjekk at dependencies er installert.")
        return

    # Show instructions
    show_testnet_instructions(wallet_info)
    show_env_configuration(wallet_info)

    # Offer to save
    save_wallet_to_file(wallet_info)

    # Final instructions
    print("\n" + "=" * 70)
    print("NESTE STEG")
    print("=" * 70)
    print("\n1. ✅ Kopier private key til .env filen")
    print("2. 🌐 Gå til Hyperliquid Discord og få testnet tokens")
    print("3. ✅ Kjør: python scripts/check_testnet_balance.py")
    print("4. 🧪 Kjør: python tests/test_03_hyperliquid_api.py")
    print("5. 🚀 Hvis alt er OK, kjør: python tests/test_all.py")

    print("\n" + "🎉" * 35)
    print("Setup klar! Lykke til med testnet trading!")
    print("🎉" * 35 + "\n")


if __name__ == "__main__":
    main()
