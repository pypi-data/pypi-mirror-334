import os
import secrets
import hashlib
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC as HMAC_PRIMITIVE

class demon:
    def __init__(self):
        self.backend = default_backend()

        # Generate Identity Key Pair (IK) using X25519 for key exchange
        self.identity_private_key = x25519.X25519PrivateKey.generate()
        self.identity_public_key = self.identity_private_key.public_key()

        # Generate Ed25519 Key Pair for digital signatures
        self.ed25519_private_key = ed25519.Ed25519PrivateKey.generate()
        self.ed25519_public_key = self.ed25519_private_key.public_key()

        self.current_session_keys = {}
        self.replay_protection_store = {}

    def generate_signed_prekey(self):
        """Generate a Signed PreKey (SPK) using X25519."""
        self.signed_prekey_private = x25519.X25519PrivateKey.generate()
        self.signed_prekey_public = self.signed_prekey_private.public_key()
        return self.signed_prekey_public

    def generate_onetime_prekey(self):
        """Generate a One-Time PreKey (OPK) using X25519."""
        self.onetime_prekey_private = x25519.X25519PrivateKey.generate()
        self.onetime_prekey_public = self.onetime_prekey_private.public_key()
        return self.onetime_prekey_public

    def rotate_session_keys(self, recipient_identity_public_key, recipient_signed_prekey_public, recipient_onetime_prekey_public):
        """Establish a shared session key using Diffie-Hellman key exchange."""
        shared_secret1 = self.identity_private_key.exchange(recipient_identity_public_key)
        shared_secret2 = self.identity_private_key.exchange(recipient_signed_prekey_public)
        shared_secret3 = self.identity_private_key.exchange(recipient_onetime_prekey_public)

        # Derive a 256-bit session key using HKDF
        session_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'session key',
            backend=self.backend
        ).derive(shared_secret1 + shared_secret2 + shared_secret3)

        self.current_session_keys = {'session_key': session_key}
        return self.identity_public_key

    def encrypt(self, content, recipient_identity_public_key, recipient_signed_prekey_public, recipient_onetime_prekey_public, is_file=False):
        """Encrypts a message or file content using the derived session key."""
        self.rotate_session_keys(recipient_identity_public_key, recipient_signed_prekey_public, recipient_onetime_prekey_public)

        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(self.current_session_keys['session_key']), modes.GCM(nonce), backend=self.backend)
        encryptor = cipher.encryptor()

        if is_file:
            with open(content, 'rb') as file:
                file_content = file.read()
            padded_content = file_content
        else:
            padder = sym_padding.PKCS7(128).padder()
            padded_content = padder.update(content.encode()) + padder.finalize()

        ciphertext = encryptor.update(padded_content) + encryptor.finalize()

        return {
            'nonce': nonce.hex(),
            'ciphertext': ciphertext.hex(),
            'tag': encryptor.tag.hex(),
        }

    def decrypt(self, encrypted_content):
        """Decrypts an encrypted message using the session key."""
        nonce = bytes.fromhex(encrypted_content['nonce'])
        tag = bytes.fromhex(encrypted_content['tag'])
        ciphertext = bytes.fromhex(encrypted_content['ciphertext'])

        cipher = Cipher(algorithms.AES(self.current_session_keys['session_key']), modes.GCM(nonce, tag), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted_padded_content = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = sym_padding.PKCS7(128).unpadder()
        decrypted_content = unpadder.update(decrypted_padded_content) + unpadder.finalize()

        return decrypted_content.decode()

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
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=3072,
            backend=self.backend
        )
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
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        ciphertext = encryptor.update(private_key_bytes) + encryptor.finalize()
        return {
            'ciphertext': ciphertext.hex(),
            'nonce': cipher.algorithm.mode.nonce.hex(),
            'tag': encryptor.tag.hex(),
            'salt': salt.hex()
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
                bytes.fromhex(encrypted_private_key['nonce']),
                bytes.fromhex(encrypted_private_key['tag'])
            ),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        private_key_bytes = decryptor.update(bytes.fromhex(encrypted_private_key['ciphertext'])) + decryptor.finalize()
        return serialization.load_pem_private_key(private_key_bytes, password=None, backend=self.backend)

    def hide_ip(self, message, ip_address):
        """Adds an IP hash to a message for privacy."""
        return f"{message} [IP: {hashlib.sha256(ip_address.encode()).hexdigest()}]"

    def verify_ip_hash(self, message, ip_hash, ip_address):
        """Verifies the IP hash for the message."""
        return hashlib.sha256(ip_address.encode()).hexdigest() == ip_hash

    # Methods for socket integration
    def initiate_key_exchange(self):
        """Initiate key exchange and return the public key to be sent to the recipient."""
        return self.identity_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def receive_key_exchange(self, recipient_public_key_bytes):
        """Receive recipient's public key and rotate session keys."""
        recipient_public_key = serialization.load_pem_public_key(
            recipient_public_key_bytes,
            backend=self.backend
        )
        self.rotate_session_keys(recipient_public_key)

    def prepare_message(self, message, recipient_identity_public_key_bytes, recipient_signed_prekey_public_bytes, recipient_onetime_prekey_public_bytes):
        """Prepare an encrypted message for sending via socket."""
        recipient_identity_public_key = serialization.load_pem_public_key(
            recipient_identity_public_key_bytes,
            backend=self.backend
        )
        recipient_signed_prekey_public = serialization.load_pem_public_key(
            recipient_signed_prekey_public_bytes,
            backend=self.backend
        )
        recipient_onetime_prekey_public = serialization.load_pem_public_key(
            recipient_onetime_prekey_public_bytes,
            backend=self.backend
        )
        return self.encrypt(message, recipient_identity_public_key, recipient_signed_prekey_public, recipient_onetime_prekey_public)

    def process_received_message(self, encrypted_content):
        """Process a received encrypted message."""
        return self.decrypt(encrypted_content, self.identity_private_key)