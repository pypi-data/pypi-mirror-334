# File: encryptionx/encode.py
from encryptionx.utils import read_input, write_output
from encryptionx.algorithms import base, hash_algo, symmetric, asymmetric, protocols

class Encode:
    def __init__(self, key=None, public_key=None):
        self.key = key
        self.public_key = public_key

    # Base encoding methods
    def base64(self, data, mode='text', output=None):
        # Read input data
        raw = read_input(data, mode)
        # Encrypt using base64 encoding
        result = base.encrypt_base64(raw)
        # Write output if specified
        write_output(result, mode, output)
        return result

    def base32(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = base.encrypt_base32(raw)
        write_output(result, mode, output)
        return result

    def base16(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = base.encrypt_base16(raw)
        write_output(result, mode, output)
        return result

    # Hash methods (one-way functions)
    def md5(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = hash_algo.encrypt_md5(raw)
        write_output(result, mode, output)
        return result

    def sha256(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = hash_algo.encrypt_sha256(raw)
        write_output(result, mode, output)
        return result

    # Symmetric encryption methods
    def aes(self, data, mode='text', output=None, key=None, iv=None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = symmetric.aes_encrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def des(self, data, mode='text', output=None, key=None, iv=None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = symmetric.des_encrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def triple_des(self, data, mode='text', output=None, key=None, iv=None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = symmetric.triple_des_encrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def rc4(self, data, mode='text', output=None, key=None):
        raw = read_input(data, mode)
        result = symmetric.rc4_encrypt(raw, key=key or self.key)
        write_output(result, mode, output)
        return result

    # Asymmetric encryption methods
    def rsa(self, data, mode='text', output=None, public_key=None):
        raw = read_input(data, mode)
        result = asymmetric.rsa_encrypt(raw, public_key=public_key or self.public_key)
        write_output(result, mode, output)
        return result

    # Protocol-based encryption methods
    def pgp(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = protocols.pgp_encrypt(raw)
        write_output(result, mode, output)
        return result
