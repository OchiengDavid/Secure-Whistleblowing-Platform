import nacl.public
from nacl.public import PrivateKey, SealedBox

try:
    # 1. Try to open the keys you just made
    with open("private_key.key", "rb") as f:
        sk = PrivateKey(f.read())
    with open("public_key.key", "rb") as f:
        pk = sk.public_key 

    # 2. Try to 'Lock' a test message
    sb = SealedBox(pk)
    secret = "Testing the Zero Knowledge Proof"
    encrypted = sb.encrypt(secret.encode())

    # 3. Try to 'Unlock' it
    unsealer = SealedBox(sk)
    decrypted = unsealer.decrypt(encrypted).decode()

    if decrypted == secret:
        print(" SUCCESS: Your keys are perfectly matched and ready!")
except Exception as e:
    print(f" ERROR: Something went wrong: {e}")