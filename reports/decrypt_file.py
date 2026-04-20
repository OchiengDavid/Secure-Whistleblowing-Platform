import nacl.public
import nacl.encoding
import sys
import os

def decrypt_leak(file_path, private_key_hex):
    if not os.path.exists(file_path):
        print(f"ERROR: File not found at {file_path}")
        return

    # 1. Setup the key
    try:
        priv_key = nacl.public.PrivateKey(private_key_hex, nacl.encoding.HexEncoder)
        unseal_box = nacl.public.SealedBox(priv_key)
        
        # 2. Read the encrypted noise
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()

        # 3. Decrypt
        decrypted_data = unseal_box.decrypt(encrypted_data)
        
        # 4. Save the result
        output_name = "RESTORED_LEAK.png"
        with open(output_name, 'wb') as f:
            f.write(decrypted_data)
        
        print(f"SUCCESS! Decrypted file saved as: {output_name}")
        
    except Exception as e:
        print(f"DECRYPTION FAILED: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 decrypt_file.py <path_to_file> <private_key>")
    else:
        decrypt_leak(sys.argv[1], sys.argv[2])