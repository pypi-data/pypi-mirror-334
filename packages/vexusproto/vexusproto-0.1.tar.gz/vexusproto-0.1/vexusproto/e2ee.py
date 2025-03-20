import os
import secrets
import base64
import hashlib
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC as HMAC_PRIMITIVE

class E2EEChatProtocol:
    def __init__(self):
        self.backend = default_backend()

        # Generate RSA private/public key for long-term identity and ECC keys
        self.ed25519_private_key = ed25519.Ed25519PrivateKey.generate()
        self.ed25519_public_key = self.ed25519_private_key.public_key()

        
        self.x25519_private_key = x25519.X25519PrivateKey.generate()
        self.x25519_public_key = self.x25519_private_key.public_key()

        self.current_session_keys = {}

    def generate_ephemeral_key_pair(self):
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        return private_key, public_key

    def rotate_session_keys(self, recipient_public_key):

        ephemeral_private_key, ephemeral_public_key = self.generate_ephemeral_key_pair()
        shared_key = ephemeral_private_key.exchange(recipient_public_key)

        # Derive a new session key using HKDF for each message exchange
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'session data',
            backend=self.backend
        ).derive(shared_key)

        # Store the keys for the current session
        self.current_session_keys = {
            'ephemeral_private_key': ephemeral_private_key,
            'ephemeral_public_key': ephemeral_public_key,
            'derived_key': derived_key
        }

        return ephemeral_public_key

    def encrypt_message(self, message, recipient_public_key):
        """Encrypts a message for the recipient with forward secrecy."""
        ephemeral_public_key = self.rotate_session_keys(recipient_public_key)

        cipher = Cipher(
            algorithms.AES(self.current_session_keys['derived_key']),
            modes.GCM(os.urandom(12)),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        padder = sym_padding.PKCS7(128).padder()
        padded_message = padder.update(message.encode()) + padder.finalize()
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()

        # Return serialized message with nonce, tag, and ciphertext
        encrypted_message = {
            'ephemeral_public_key': ephemeral_public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            ),
            'nonce': cipher.algorithm.mode.nonce,
            'ciphertext': ciphertext,
            'tag': encryptor.tag
        }
        return json.dumps(encrypted_message)

    def decrypt_message(self, encrypted_message, private_key):
        """Decrypts a message and ensures message integrity and freshness."""
        encrypted_message = json.loads(encrypted_message)
        ephemeral_public_key = x25519.X25519PublicKey.from_public_bytes(
            encrypted_message['ephemeral_public_key']
        )
        shared_key = private_key.exchange(ephemeral_public_key)

        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'session data',
            backend=self.backend
        ).derive(shared_key)

        cipher = Cipher(
            algorithms.AES(derived_key),
            modes.GCM(
                encrypted_message['nonce'],
                encrypted_message['tag']
            ),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        decrypted_padded_message = decryptor.update(encrypted_message['ciphertext']) + decryptor.finalize()
        unpadder = sym_padding.PKCS7(128).unpadder()
        decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

        return decrypted_message.decode()

    def sign_message(self, message):
        """Signs a message with Ed25519 to ensure authenticity."""
        return self.ed25519_private_key.sign(message.encode())

    def verify_signature(self, message, signature, public_key):
        """Verifies the authenticity of a message."""
        try:
            public_key.verify(signature, message.encode())
            return True
        except:
            return False

    def generate_replay_protection_token(self, message):
        """Generates a token to protect against message replay."""
        return hashlib.sha256(message.encode()).digest()

    def verify_replay_protection_token(self, message, token):
        """Verifies if a message has been replayed."""
        return hashlib.sha256(message.encode()).digest() == token

    def create_user_key_pair(self, password):
        """Generates a user-specific key pair based on a password."""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        key = kdf.derive(password.encode())
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        return private_key, public_key, key, salt

    def encrypt_user_private_key(self, private_key, key, salt):
        """Encrypts a user private key using AES."""
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(os.urandom(12)),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        ciphertext = encryptor.update(private_key_bytes) + encryptor.finalize()
        return {
            'ciphertext': ciphertext,
            'nonce': cipher.algorithm.mode.nonce,
            'tag': encryptor.tag,
            'salt': salt
        }

    def decrypt_user_private_key(self, encrypted_private_key, password, salt):
        """Decrypts a user private key using AES."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        key = kdf.derive(password.encode())
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(
                encrypted_private_key['nonce'],
                encrypted_private_key['tag']
            ),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        private_key_bytes = decryptor.update(encrypted_private_key['ciphertext']) + decryptor.finalize()
        return x25519.X25519PrivateKey.from_private_bytes(private_key_bytes)

    def hide_ip(self, message, ip_address):
        """Adds an IP hash to a message for privacy."""
        return f"{message} [IP: {hashlib.sha256(ip_address.encode()).hexdigest()}]"

    def verify_ip_hash(self, message, ip_hash, ip_address):
        """Verifies the IP hash for the message."""
        return hashlib.sha256(ip_address.encode()).hexdigest() == ip_hash
