import os
import secrets
import hashlib
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC as HMAC_PRIMITIVE
from doubleratchet.double_ratchet import DoubleRatchet
from doubleratchet.diffie_hellman_ratchet import DiffieHellmanRatchet
from doubleratchet.kdf import KDF
from doubleratchet.aead import AEAD, AuthenticationFailedException, DecryptionFailedException

class demon:
    def __init__(self):
        self.backend = default_backend()

        # Generate Identity Key Pair (IK) using X25519 for forward secrecy
        self.identity_private_key = x25519.X25519PrivateKey.generate()
        self.identity_public_key = self.identity_private_key.public_key()

        # Generate Ed25519 Key Pair for digital signatures
        self.ed25519_private_key = ed25519.Ed25519PrivateKey.generate()
        self.ed25519_public_key = self.ed25519_private_key.public_key()

        self.current_session_keys = {}
        self.double_ratchet = None

        # Store previously seen replay protection tokens
        self.replay_protection_store = {}

    def generate_signed_prekey(self):
        # Generate Signed PreKey Pair (SPK)
        self.signed_prekey_private = x25519.X25519PrivateKey.generate()
        self.signed_prekey_public = self.signed_prekey_private.public_key()
        return self.signed_prekey_public

    def generate_onetime_prekey(self):
        # Generate One-Time PreKey Pair (OPK)
        self.onetime_prekey_private = x25519.X25519PrivateKey.generate()
        self.onetime_prekey_public = self.onetime_prekey_private.public_key()
        return self.onetime_prekey_public

    def sign_message(self, message):
        """Signs the message with the Ed25519 private key."""
        signature = self.ed25519_private_key.sign(message.encode())
        return signature

    def verify_signature(self, message, signature, public_key):
        """Verifies the signature using the Ed25519 public key."""
        try:
            public_key.verify(signature, message.encode())
            return True  # Signature is valid
        except Exception:
            return False  # Signature is invalid

    async def initialize_double_ratchet(self, shared_secret, recipient_ratchet_pub):
        """Initialize the Double Ratchet with the recipient's public key and shared secret."""
        self.double_ratchet, _ = await DoubleRatchet.encrypt_initial_message(
            diffie_hellman_ratchet_class=DiffieHellmanRatchet,
            root_chain_kdf=KDF,
            message_chain_kdf=KDF,
            message_chain_constant=b'double_ratchet',
            dos_protection_threshold=1000,
            max_num_skipped_message_keys=100,
            aead=AEAD,
            shared_secret=shared_secret,
            recipient_ratchet_pub=recipient_ratchet_pub,
            message=b'initial message',
            associated_data=b'init'
        )

    async def encrypt(self, content, associated_data=b''):
        """Encrypts a message or file content for the recipient with forward secrecy."""
        if not self.double_ratchet:
            raise ValueError("Double Ratchet not initialized. Call initialize_double_ratchet first.")

        # Generate a nonce (IV) for GCM mode
        nonce = os.urandom(12)

        # Create the cipher with the nonce
        cipher = Cipher(
            algorithms.AES(self.current_session_keys['derived_key']),
            modes.GCM(nonce),
            backend=self.backend
        )

        encryptor = cipher.encryptor()

        # Apply padding for AES encryption
        padder = sym_padding.PKCS7(128).padder()
        padded_content = padder.update(content.encode()) + padder.finalize()

        # Encrypt the padded content
        ciphertext = encryptor.update(padded_content) + encryptor.finalize()

        # Encrypt the message with Double Ratchet
        encrypted_message = await self.double_ratchet.encrypt_message(content.encode(), associated_data)

        # Generate HMAC for message integrity
        hmac = HMAC_PRIMITIVE(self.current_session_keys['derived_key'], hashes.SHA256(), backend=self.backend)
        hmac.update(ciphertext)
        hmac_value = hmac.finalize()

        # Generate the replay protection token
        token = self.generate_replay_protection_token(content, self.identity_public_key)

        # Return serialized content with nonce, tag, ciphertext in hex, replay protection token, and HMAC
        encrypted_content = {
            'double_ratchet': encrypted_message,
            'nonce': nonce.hex(),  # Convert nonce to hex
            'ciphertext': ciphertext.hex(),  # Convert ciphertext to hex
            'tag': encryptor.tag.hex(),  # Convert tag to hex
            'replay_token': token,  # Include the replay protection token
            'hmac': hmac_value.hex()  # Include the HMAC
        }
        return encrypted_content

    async def decrypt(self, encrypted_content, associated_data=b''):
        """Decrypts a message or file content and ensures message integrity and freshness."""
        if not self.double_ratchet:
            raise ValueError("Double Ratchet not initialized. Call initialize_double_ratchet first.")

        nonce = bytes.fromhex(encrypted_content['nonce'])
        tag = bytes.fromhex(encrypted_content['tag'])
        ciphertext = bytes.fromhex(encrypted_content['ciphertext'])
        encrypted_message = encrypted_content['double_ratchet']

        # Decrypt the message with Double Ratchet
        decrypted_message = await self.double_ratchet.decrypt_message(encrypted_message, associated_data)

        cipher = Cipher(
            algorithms.AES(self.current_session_keys['derived_key']),
            modes.GCM(nonce, tag),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        decrypted_padded_content = decryptor.update(ciphertext) + decryptor.finalize()

        # Unpad the content
        unpadder = sym_padding.PKCS7(128).unpadder()
        decrypted_content = unpadder.update(decrypted_padded_content) + unpadder.finalize()

        # Verify the replay protection token
        token = encrypted_content['replay_token']
        if not self.verify_replay_protection_token(decrypted_content.decode(), token, self.identity_public_key):
            raise Exception("Replay detected. The message has been replayed.")

        # Verify the HMAC
        hmac = HMAC_PRIMITIVE(self.current_session_keys['derived_key'], hashes.SHA256(), backend=self.backend)
        hmac.update(ciphertext)
        hmac.verify(bytes.fromhex(encrypted_content['hmac']))

        return decrypted_content.decode()  # Return decrypted content as text

    def generate_replay_protection_token(self, message, recipient_public_key):
        """Generates a token to protect against message replay, using timestamp and nonce."""
        timestamp = int(time.time())
        nonce = secrets.token_bytes(16)  # Generate a 16-byte random nonce
        message_hash = hashlib.sha256(message.encode()).hexdigest()

        token = {
            'message_hash': message_hash,
            'timestamp': timestamp,
            'nonce': nonce.hex()
        }

        recipient_key = recipient_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).hex()
        
        if recipient_key not in self.replay_protection_store:
            self.replay_protection_store[recipient_key] = []

        self.replay_protection_store[recipient_key].append(token)

        return token

    def verify_replay_protection_token(self, message, token, recipient_public_key):
        """Verifies if a message has been replayed using the stored token data."""
        recipient_key = recipient_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).hex()

        stored_tokens = self.replay_protection_store.get(recipient_key, [])

        message_hash = hashlib.sha256(message.encode()).hexdigest()

        for stored_token in stored_tokens:
            if stored_token['message_hash'] == message_hash and stored_token['nonce'] == token['nonce']:
                # If we find the same message hash with the same nonce, this is a replay
                return False

        # If token is not found or the nonce is different, this message is new
        return True

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

    async def receive_key_exchange(self, recipient_public_key_bytes, shared_secret):
        """Receive recipient's public key and initialize Double Ratchet."""
        recipient_public_key = serialization.load_pem_public_key(
            recipient_public_key_bytes,
            backend=self.backend
        )
        await self.initialize_double_ratchet(shared_secret, recipient_public_key.public_bytes(
            encoding=serialization.Encoding.Raw  # Correcting the issue here
        ))

    async def prepare_message(self, message, associated_data=b''):
        """Prepare an encrypted message for sending via socket."""
        return await self.encrypt(message, associated_data)

    async def process_received_message(self, encrypted_content, associated_data=b''):
        """Process a received encrypted message."""
        return await self.decrypt(encrypted_content, associated_data)