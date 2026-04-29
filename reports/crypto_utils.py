import nacl.public
import os
from django.conf import settings

def seal_report(message_text):
    """
    Takes plain text and returns an encrypted blob using the Public Key.
    """
    # 1. Locate the Public Key
    # We assume it's in your main project folder
    key_path = os.path.join(settings.BASE_DIR, 'Secure-Whistleblowing-Platform', 'public_key.key')
    
    # If the path above is tricky, you can also use a simple relative path for now:
    # key_path = "public_key.key"

    with open(key_path, "rb") as f:
        public_key_data = f.read()
    
    public_key = nacl.public.PublicKey(public_key_data)
    
    # 2. Create the Sealed Box
    sealed_box = nacl.public.SealedBox(public_key)
    
    # 3. Encrypt the message (must be bytes)
    encrypted_bytes = sealed_box.encrypt(message_text.encode('utf-8'))
    
    return encrypted_bytes