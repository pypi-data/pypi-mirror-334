# File: encryptionx/decode.py
from encryptionx.utils import read_input, write_output
from encryptionx.algorithms import base, symmetric, asymmetric, protocols

class Decode:
    def __init__(self, key=None, private_key=None):
        self.key = key
        self.private_key = private_key

    # Base decoding methods
    def base64(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = base.decrypt_base64(raw)
        write_output(result, mode, output)
        return result

    def base32(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = base.decrypt_base32(raw)
        write_output(result, mode, output)
        return result

    def base16(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = base.decrypt_base16(raw)
        write_output(result, mode, output)
        return result

    # Hash functions are one-way; decryption is not possible
    def md5(self, data, mode='text', output=None):
        raise Exception("Hash functions are one-way and cannot be decrypted.")

    def sha256(self, data, mode='text', output=None):
        raise Exception("Hash functions are one-way and cannot be decrypted.")

    # Symmetric decryption methods
    def aes(self, data, mode='text', output=None, key=None, iv=None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = symmetric.aes_decrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def des(self, data, mode='text', output=None, key=None, iv=None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = symmetric.des_decrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def triple_des(self, data, mode='text', output=None, key=None, iv=None, cipher_mode='CBC'):
        raw = read_input(data, mode)
        result = symmetric.triple_des_decrypt(raw, key=key or self.key, iv=iv, cipher_mode=cipher_mode)
        write_output(result, mode, output)
        return result

    def rc4(self, data, mode='text', output=None, key=None):
        raw = read_input(data, mode)
        result = symmetric.rc4_decrypt(raw, key=key or self.key)
        write_output(result, mode, output)
        return result

    # Asymmetric decryption methods
    def rsa(self, data, mode='text', output=None, private_key=None):
        raw = read_input(data, mode)
        result = asymmetric.rsa_decrypt(raw, private_key=private_key or self.private_key)
        write_output(result, mode, output)
        return result

    # Protocol-based decryption methods
    def pgp(self, data, mode='text', output=None):
        raw = read_input(data, mode)
        result = protocols.pgp_decrypt(raw)
        write_output(result, mode, output)
        return result
