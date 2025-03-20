# EncryptionX

EncryptionX is a comprehensive encryption library for Python that supports a wide range of encryption and decryption algorithms including base encoding, hashing, symmetric and asymmetric encryption, and protocol-based encryption such as PGP.

## Features

- **Base Encoding:** Base16, Base32, Base64
- **Hashing:** MD5, SHA256
- **Symmetric Encryption:** AES, DES, Triple DES, RC4
- **Asymmetric Encryption:** RSA
- **Protocol Encryption:** PGP

## Installation

You can install the package via pip:

```bash
pip install encryptionx
Usage Example
python
Copy
Edit
from encryptionx.encode import Encode
from encryptionx.decode import Decode

# Define a symmetric key (16 bytes for AES)
symmetric_key = b'0123456789abcdef'

# Create encoder and decoder instances
encoder = Encode(key=symmetric_key)
decoder = Decode(key=symmetric_key)

# Encrypt and decrypt a sample text using AES
sample_text = "Hello, EncryptionX!"
encrypted = encoder.aes(sample_text, mode='text', cipher_mode='CBC')
decrypted = decoder.aes(encrypted, mode='text', cipher_mode='CBC')

print("Encrypted (AES):", encrypted)
print("Decrypted (AES):", decrypted.decode('utf-8'))
Requirements
Python 3.6+
PyCryptodome
Author
Mohammad Taha Gorji