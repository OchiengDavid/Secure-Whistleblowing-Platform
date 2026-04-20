import nacl.public
import nacl.encoding
import sys
import os

def decrypt_leak(file_path, private_key_hex):
    # Setup keys
    priv_key = nacl.public.PrivateKey(private_key_hex, nacl.encoding.HexEncoder)
    unseal_box = nacl.public.SealedBox(priv_key)
    
    # Read and decrypt
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    
    decrypted_data = unseal_box.decrypt(encrypted_data)
    
    # Save the output
    output_name = "RESTORED_IMAGE.png"
    with open(output_name, 'wb') as f:
        f.write(decrypted_data)
    print(f"DONE! Decrypted file saved as {output_name}")

if __name__ == "__main__":
    decrypt_leak(sys.argv[1], sys.argv[2])