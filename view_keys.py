import nacl.public

# 1. Read the 'Lock' (Public Key)
with open("public_key.key", "rb") as f:
    public_hex = f.read().hex()
    print(f"--- PUBLIC KEY (The Lock) ---")
    print(public_hex)
    print("------------------------------\n")

# 2. Read the 'Key' (Private Key)
with open("private_key.key", "rb") as f:
    private_hex = f.read().hex()
    print(f"--- PRIVATE KEY (The Secret) ---")
    print(private_hex)
    print("--------------------------------")