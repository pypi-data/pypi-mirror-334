"""
EncryptionX - A Comprehensive Encryption Library in a Single File
Author: Mohammad Taha Gorji
Version: 2.0.0

This library provides various encryption and decryption methods including:
- Base encoding: Base64, Base32, Base16
- Hashing: MD5, SHA256
- Symmetric encryption: AES, DES, Triple DES, RC4
- Asymmetric encryption: RSA
- Protocol-based encryption: PGP

Dependencies:
- pycryptodome

To install dependency:
    pip install pycryptodome
"""

import os
import io
import zipfile
import base64
import hashlib
from Crypto.Cipher import AES, DES, DES3, PKCS1_OAEP
from Crypto.PublicKey import RSA

#########################
# Utility Functions
#########################
def read_input(data, mode):
    """
    Read input data based on mode.
    Modes: 'text', 'file', 'folder'
    """
    if mode == 'text':
        return data.encode('utf-8')
    elif mode == 'file':
        with open(data, 'rb') as f:
            return f.read()
    elif mode == 'folder':
        # Compress folder into a zip archive in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(data):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, data)
                    zip_file.write(file_path, arcname)
        return zip_buffer.getvalue()
    else:
        raise ValueError("Invalid mode. Use 'text', 'file', or 'folder'.")

def write_output(data, mode, output):
    """
    Write output data based on mode.
    Modes: 'text', 'file', 'folder'
    """
    if output is None:
        return data
    if mode == 'text':
        with open(output, 'w', encoding='utf-8') as f:
            f.write(data.decode('utf-8'))
    elif mode == 'file':
        with open(output, 'wb') as f:
            f.write(data)
    elif mode == 'folder':
        # Assume data is a zip archive; extract to output folder
        with zipfile.ZipFile(io.BytesIO(data), 'r') as zip_file:
            zip_file.extractall(output)
    else:
        raise ValueError("Invalid mode. Use 'text', 'file', or 'folder'.")


#########################
# Base Encoding Functions
#########################
def encrypt_base64(data: bytes) -> bytes:
    return base64.b64encode(data)

def decrypt_base64(data: bytes) -> bytes:
    return base64.b64decode(data)

def encrypt_base32(data: bytes) -> bytes:
    return base64.b32encode(data)

def decrypt_base32(data: bytes) -> bytes:
    return base64.b32decode(data)

def encrypt_base16(data: bytes) -> bytes:
    return base64.b16encode(data)

def decrypt_base16(data: bytes) -> bytes:
    return base64.b16decode(data)


#########################
# Hash Functions
#########################
def encrypt_md5(data: bytes) -> bytes:
    hash_obj = hashlib.md5(data)
    return hash_obj.hexdigest().encode('utf-8')

def encrypt_sha256(data: bytes) -> bytes:
    hash_obj = hashlib.sha256(data)
    return hash_obj.hexdigest().encode('utf-8')


#########################
# Symmetric Encryption Functions
#########################
# AES Encryption/Decryption
def aes_encrypt(data: bytes, key: bytes, iv: bytes = None, cipher_mode='CBC') -> bytes:
    if key is None:
        raise ValueError("AES key is required.")
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes long.")
    if cipher_mode.upper() == 'CBC':
        iv = iv or (b'\x00' * 16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pad_len = 16 - (len(data) % 16)
        data += bytes([pad_len]) * pad_len
        return cipher.encrypt(data)
    elif cipher_mode.upper() == 'ECB':
        cipher = AES.new(key, AES.MODE_ECB)
        pad_len = 16 - (len(data) % 16)
        data += bytes([pad_len]) * pad_len
        return cipher.encrypt(data)
    else:
        raise NotImplementedError("AES mode not supported.")

def aes_decrypt(data: bytes, key: bytes, iv: bytes = None, cipher_mode='CBC') -> bytes:
    if key is None:
        raise ValueError("AES key is required.")
    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes long.")
    if cipher_mode.upper() == 'CBC':
        iv = iv or (b'\x00' * 16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(data)
        pad_len = decrypted[-1]
        return decrypted[:-pad_len]
    elif cipher_mode.upper() == 'ECB':
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(data)
        pad_len = decrypted[-1]
        return decrypted[:-pad_len]
    else:
        raise NotImplementedError("AES mode not supported.")

# DES Encryption/Decryption
def des_encrypt(data: bytes, key: bytes, iv: bytes = None, cipher_mode='CBC') -> bytes:
    if key is None or len(key) != 8:
        raise ValueError("DES key must be 8 bytes long.")
    if cipher_mode.upper() == 'CBC':
        iv = iv or (b'\x00' * 8)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        pad_len = 8 - (len(data) % 8)
        data += bytes([pad_len]) * pad_len
        return cipher.encrypt(data)
    elif cipher_mode.upper() == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
        pad_len = 8 - (len(data) % 8)
        data += bytes([pad_len]) * pad_len
        return cipher.encrypt(data)
    else:
        raise NotImplementedError("DES mode not supported.")

def des_decrypt(data: bytes, key: bytes, iv: bytes = None, cipher_mode='CBC') -> bytes:
    if key is None or len(key) != 8:
        raise ValueError("DES key must be 8 bytes long.")
    if cipher_mode.upper() == 'CBC':
        iv = iv or (b'\x00' * 8)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        decrypted = cipher.decrypt(data)
        pad_len = decrypted[-1]
        return decrypted[:-pad_len]
    elif cipher_mode.upper() == 'ECB':
        cipher = DES.new(key, DES.MODE_ECB)
        decrypted = cipher.decrypt(data)
        pad_len = decrypted[-1]
        return decrypted[:-pad_len]
    else:
        raise NotImplementedError("DES mode not supported.")

# Triple DES Encryption/Decryption
def triple_des_encrypt(data: bytes, key: bytes, iv: bytes = None, cipher_mode='CBC') -> bytes:
    if key is None or len(key) not in (16, 24):
        raise ValueError("Triple DES key must be 16 or 24 bytes long.")
    if cipher_mode.upper() == 'CBC':
        iv = iv or (b'\x00' * 8)
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        pad_len = 8 - (len(data) % 8)
        data += bytes([pad_len]) * pad_len
        return cipher.encrypt(data)
    elif cipher_mode.upper() == 'ECB':
        cipher = DES3.new(key, DES3.MODE_ECB)
        pad_len = 8 - (len(data) % 8)
        data += bytes([pad_len]) * pad_len
        return cipher.encrypt(data)
    else:
        raise NotImplementedError("Triple DES mode not supported.")

def triple_des_decrypt(data: bytes, key: bytes, iv: bytes = None, cipher_mode='CBC') -> bytes:
    if key is None or len(key) not in (16, 24):
        raise ValueError("Triple DES key must be 16 or 24 bytes long.")
    if cipher_mode.upper() == 'CBC':
        iv = iv or (b'\x00' * 8)
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        decrypted = cipher.decrypt(data)
        pad_len = decrypted[-1]
        return decrypted[:-pad_len]
    elif cipher_mode.upper() == 'ECB':
        cipher = DES3.new(key, DES3.MODE_ECB)
        decrypted = cipher.decrypt(data)
        pad_len = decrypted[-1]
        return decrypted[:-pad_len]
    else:
        raise NotImplementedError("Triple DES mode not supported.")

# RC4 Encryption/Decryption
def rc4_encrypt(data: bytes, key: bytes) -> bytes:
    S = list(range(256))
    j = 0
    out = []
    # Key-Scheduling Algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    # Pseudo-Random Generation Algorithm (PRGA)
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(byte ^ K)
    return bytes(out)

def rc4_decrypt(data: bytes, key: bytes) -> bytes:
    # RC4 encryption and decryption are identical
    return rc4_encrypt(data, key)


#########################
# Asymmetric Encryption Functions (RSA)
#########################
def generate_rsa_keys(key_size: int = 2048):
    """
    Generate RSA key pair.
    Returns (public_key, private_key) as bytes.
    """
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return public_key, private_key

def rsa_encrypt(data: bytes, public_key: bytes) -> bytes:
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted = cipher.encrypt(data)
    return base64.b64encode(encrypted)

def rsa_decrypt(data: bytes, private_key: bytes) -> bytes:
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted = base64.b64decode(data)
    decrypted = cipher.decrypt(encrypted)
    return decrypted


#########################
# Protocol-based Encryption Functions (PGP Demo)
#########################
_default_rsa_public = None
_default_rsa_private = None

def _generate_default_rsa_keys():
    global _default_rsa_public, _default_rsa_private
    key = RSA.generate(2048)
    _default_rsa_private = key.export_key()
    _default_rsa_public = key.publickey().export_key()

def pgp_encrypt(data: bytes, public_key: bytes = None) -> bytes:
    global _default_rsa_public
    if public_key is None:
        if _default_rsa_public is None:
            _generate_default_rsa_keys()
        public_key = _default_rsa_public
    # Generate a random AES key and IV
    aes_key = os.urandom(16)
    iv = os.urandom(16)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    pad_len = 16 - (len(data) % 16)
    padded_data = data + bytes([pad_len]) * pad_len
    encrypted_data = cipher_aes.encrypt(padded_data)
    # Encrypt the AES key using RSA
    rsa_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)
    # Package the encrypted AES key, IV, and data (all base64-encoded)
    package = (base64.b64encode(encrypted_key) + b':::' +
               base64.b64encode(iv) + b':::' +
               base64.b64encode(encrypted_data))
    return package

def pgp_decrypt(package: bytes, private_key: bytes = None) -> bytes:
    global _default_rsa_private
    if private_key is None:
        if _default_rsa_private is None:
            raise ValueError("Private key is required for PGP decryption.")
        private_key = _default_rsa_private
    try:
        parts = package.split(b':::')
        if len(parts) != 3:
            raise ValueError("Invalid PGP package format.")
        encrypted_key_b64, iv_b64, encrypted_data_b64 = parts
        encrypted_key = base64.b64decode(encrypted_key_b64)
        iv = base64.b64decode(iv_b64)
        encrypted_data = base64.b64decode(encrypted_data_b64)
    except Exception as e:
        raise ValueError("Error parsing PGP package: " + str(e))
    rsa_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    aes_key = cipher_rsa.decrypt(encrypted_key)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_padded = cipher_aes.decrypt(encrypted_data)
    pad_len = decrypted_padded[-1]
    return decrypted_padded[:-pad_len]


#########################
# Encode and Decode Classes
#########################
class Encode:
    def __init__(self, key: bytes = None, public_key: bytes = None):
        self.key = key
        self.public_key = public_key

    # Base encoding methods
    def base64(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = encrypt_base64(raw)
        write_output(result, mode, output)
        return result

    def base32(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = encrypt_base32(raw)
        write_output(result, mode, output)
        return result

    def base16(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = encrypt_base16(raw)
        write_output(result, mode, output)
        return result

    # Hash functions (one-way)
    def md5(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = encrypt_md5(raw)
        write_output(result, mode, output)
        return result

    def sha256(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = encrypt_sha256(raw)
        write_output(result, mode, output)
        return result

    # Symmetric encryption methods
    def aes(self, data, mode='text', output=None, key: bytes = None, iv: bytes = None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = aes_encrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def des(self, data, mode='text', output=None, key: bytes = None, iv: bytes = None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = des_encrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def triple_des(self, data, mode='text', output=None, key: bytes = None, iv: bytes = None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = triple_des_encrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def rc4(self, data, mode='text', output=None, key: bytes = None):
        raw = read_input(data, mode)
        result = rc4_encrypt(raw, key=key or self.key)
        write_output(result, mode, output)
        return result

    # Asymmetric encryption methods
    def rsa(self, data, mode='text', output=None, public_key: bytes = None):
        raw = read_input(data, mode)
        result = rsa_encrypt(raw, public_key=public_key or self.public_key)
        write_output(result, mode, output)
        return result

    # Protocol encryption (PGP)
    def pgp(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = pgp_encrypt(raw)
        write_output(result, mode, output)
        return result

class Decode:
    def __init__(self, key: bytes = None, private_key: bytes = None):
        self.key = key
        self.private_key = private_key

    # Base decoding methods
    def base64(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = decrypt_base64(raw)
        write_output(result, mode, output)
        return result

    def base32(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = decrypt_base32(raw)
        write_output(result, mode, output)
        return result

    def base16(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = decrypt_base16(raw)
        write_output(result, mode, output)
        return result

    # Hash functions are one-way; decryption is not possible.
    def md5(self, data, mode='text', output=None):
        raise Exception("Hash functions are one-way and cannot be decrypted.")

    def sha256(self, data, mode='text', output=None):
        raise Exception("Hash functions are one-way and cannot be decrypted.")

    # Symmetric decryption methods
    def aes(self, data, mode='text', output=None, key: bytes = None, iv: bytes = None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = aes_decrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def des(self, data, mode='text', output=None, key: bytes = None, iv: bytes = None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = des_decrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def triple_des(self, data, mode='text', output=None, key: bytes = None, iv: bytes = None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = triple_des_decrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def rc4(self, data, mode='text', output=None, key: bytes = None):
        raw = read_input(data, mode)
        result = rc4_decrypt(raw, key=key or self.key)
        write_output(result, mode, output)
        return result

    # Asymmetric decryption methods
    def rsa(self, data, mode='text', output=None, private_key: bytes = None):
        raw = read_input(data, mode)
        result = rsa_decrypt(raw, private_key=private_key or self.private_key)
        write_output(result, mode, output)
        return result

    # Protocol decryption (PGP)
    def pgp(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = pgp_decrypt(raw, private_key=self.private_key)
        write_output(result, mode, output)
        return result
