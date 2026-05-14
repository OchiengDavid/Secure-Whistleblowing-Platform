#!/usr/bin/env python3
"""
Encryption Key Generator for SafeReport App

This script generates public/private key pairs for encrypting/decrypting
submitted files in the SafeReport application.

Usage:
    python generate_keys.py

This will generate:
- OFFICER_PUBLIC_KEY: Used by the Django app to encrypt files
- OFFICER_PRIVATE_KEY: Used by admins to decrypt files

Add these to your environment variables or Django settings.
"""

import nacl.public
import nacl.encoding

def generate_keys():
    """Generate a new public/private key pair for encryption"""
    # Generate private key
    private_key = nacl.public.PrivateKey.generate()

    # Get corresponding public key
    public_key = private_key.public_key

    # Convert to hex format for storage
    private_hex = private_key.encode(nacl.encoding.HexEncoder).decode('ascii')
    public_hex = public_key.encode(nacl.encoding.HexEncoder).decode('ascii')

    return private_hex, public_hex

if __name__ == "__main__":
    print("SafeReport Encryption Key Generator")
    print("=" * 50)

    private_key, public_key = generate_keys()

    print("\n Keys generated successfully!")
    print("\n Add these to your environment variables:")
    print(f"\nOFFICER_PUBLIC_KEY={public_key}")
    print(f"OFFICER_PRIVATE_KEY={private_key}")

    print("\n  IMPORTANT SECURITY NOTES:")
    print("- Store the OFFICER_PRIVATE_KEY securely and privately")
    print("- Only authorized personnel should have access to the private key")
    print("- The public key can be safely shared with the Django application")
    print("- Keep backups of both keys in secure locations")

    print("\n To regenerate keys (will invalidate all previously encrypted files):")
    print("   Run this script again")

    print("\n For Django settings, you can also add to settings.py:")
    print("import os")
    print(f"os.environ['OFFICER_PUBLIC_KEY'] = '{public_key}'")
    print(f"os.environ['OFFICER_PRIVATE_KEY'] = '{private_key}'")
