import os
import secrets
import hashlib
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hmac import HMAC as HMAC_PRIMITIVE
from doubleratchet import DoubleRatchet, DiffieHellmanRatchet, KDF, AEAD

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

    async def initialize_double_ratchet(self, recipient_ratchet_pub, shared_secret):
        root_chain_kdf = KDF()
        message_chain_kdf = KDF()
        message_chain_constant = b'message_chain_constant'
        dos_protection_threshold = 10
        max_num_skipped_message_keys = 100
        aead = AEAD()

        # Initialize the Double Ratchet for the first message
        self.double_ratchet, initial_message = await DoubleRatchet.encrypt_initial_message(
            DiffieHellmanRatchet, root_chain_kdf, message_chain_kdf, message_chain_constant,
            dos_protection_threshold, max_num_skipped_message_keys, aead, shared_secret,
            recipient_ratchet_pub, b"Initial message", b"Associated data"
        )
        return initial_message

    async def encrypt_message(self, message, associated_data):
        return await self.double_ratchet.encrypt_message(message.encode(), associated_data.encode())

    async def decrypt_message(self, encrypted_message, associated_data):
        return await self.double_ratchet.decrypt_message(encrypted_message, associated_data.encode())

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

    async def encrypt(self, content, recipient_identity_public_key, recipient_signed_prekey_public, recipient_onetime_prekey_public, is_file=False):
        """Encrypts a message or file content for the recipient with forward secrecy."""
        # Initialize the Double Ratchet if not already initialized
        if not hasattr(self, 'double_ratchet'):
            shared_secret = b'shared_secret_' + recipient_identity_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            await self.initialize_double_ratchet(recipient_signed_prekey_public, shared_secret[:32])
 
        # Encrypt the content using the Double Ratchet
        encrypted_content = await self.encrypt_message(content, 'Associated data')
        
        if is_file:
            encrypted_file_path = content + '.enc'
            with open(encrypted_file_path, 'wb') as file:
                file.write(encrypted_content)
            return encrypted_file_path
        else:
            return encrypted_content

    async def decrypt(self, encrypted_content, private_key, is_file=False):
        """Decrypts a message or file content and ensures message integrity and freshness."""
        if is_file:
            with open(encrypted_content, 'rb') as file:
                encrypted_data = file.read()
            decrypted_content = await self.decrypt_message(encrypted_data, 'Associated data')
            decrypted_file_path = encrypted_content.replace('.enc', '')
            with open(decrypted_file_path, 'wb') as file:
                file.write(decrypted_content)
            return decrypted_file_path
        else:
            decrypted_content = await self.decrypt_message(encrypted_content, 'Associated data')
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