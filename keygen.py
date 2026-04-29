import nacl.utils
from nacl.public import PrivateKey
import os

# Generate a brand new Private Key
sk = PrivateKey.generate()

# Derive the Public Key from it
pk = sk.public_key

# Save the Private Key (DO NOT LOSE THIS!)
with open("private_key.key", "wb") as f:
    f.write(sk.encode())

# Save the Public Key (This stays in your Django project)
with open("public_key.key", "wb") as f:
    f.write(pk.encode())

print("Success! Two files created: public_key.key and private_key.key.")