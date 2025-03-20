import os
import secrets
import hashlib
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import dh, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC as HMAC_PRIMITIVE


class Demon:
    def __init__(self) -> None:
        self.backend = default_backend()

        # Generate Identity Key Pair (IK) using Diffie-Hellman for key exchange
        self.parameters = dh.generate_parameters(generator=2, key_size=3072, backend=self.backend)
        self.identity_private_key = self.parameters.generate_private_key()
        self.identity_public_key = self.identity_private_key.public_key()

        # Generate Ed25519 Key Pair for digital signatures
        self.ed25519_private_key = ed25519.Ed25519PrivateKey.generate()
        self.ed25519_public_key = self.ed25519_private_key.public_key()

        self.current_session_keys = {}

        # Store previously seen replay protection tokens
        self.replay_protection_store = {}

    def generate_signed_prekey(self) -> dh.DHPublicKey:
        # Generate Signed PreKey Pair (SPK)
        self.signed_prekey_private = self.parameters.generate_private_key()
        return self.signed_prekey_private.public_key()

    def generate_onetime_prekey(self) -> dh.DHPublicKey:
        # Generate One-Time PreKey Pair (OPK)
        self.onetime_prekey_private = self.parameters.generate_private_key()
        return self.onetime_prekey_private.public_key()

    def sign_message(self, message: str) -> bytes:
        """Signs the message with the Ed25519 private key."""
        return self.ed25519_private_key.sign(message.encode())

    def verify_signature(self, message: str, signature: bytes, public_key: ed25519.Ed25519PublicKey) -> bool:
        """Verifies the signature using the Ed25519 public key."""
        try:
            public_key.verify(signature, message.encode())
            return True  # Signature is valid
        except Exception:
            return False  # Signature is invalid

    def rotate_session_keys(self, recipient_identity_public_key: dh.DHPublicKey, recipient_signed_prekey_public: dh.DHPublicKey, recipient_onetime_prekey_public: dh.DHPublicKey) -> dh.DHPublicKey:
        try:
            shared_key_identity = self.identity_private_key.exchange(recipient_identity_public_key)
            shared_key_signed_prekey = self.identity_private_key.exchange(recipient_signed_prekey_public)
            shared_key_onetime_prekey = self.identity_private_key.exchange(recipient_onetime_prekey_public)

            # Combine the shared secrets from the three Diffie-Hellman exchanges
            combined_shared_key = hashlib.sha256(shared_key_identity + shared_key_signed_prekey + shared_key_onetime_prekey).digest()

            # Derive the session key using HKDF
            session_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'session data',
                backend=self.backend
            ).derive(combined_shared_key)

            self.current_session_keys = {
                'session_key': session_key,
            }

            return self.identity_public_key

        except Exception as e:
            raise ValueError(f"Error during key exchange: {e}")

    def generate_replay_protection_token(self, message: str, recipient_public_key: dh.DHPublicKey) -> dict:
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

    def verify_replay_protection_token(self, message: str, token: dict, recipient_public_key: dh.DHPublicKey) -> bool:
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

    def encrypt(self, content: str, recipient_identity_public_key: dh.DHPublicKey, recipient_signed_prekey_public: dh.DHPublicKey, recipient_onetime_prekey_public: dh.DHPublicKey, is_file: bool = False) -> dict:
        """Encrypts a message or file content for the recipient with forward secrecy."""
        ephemeral_public_key = self.rotate_session_keys(recipient_identity_public_key, recipient_signed_prekey_public, recipient_onetime_prekey_public)

        # Generate a nonce (IV) for GCM mode
        nonce = os.urandom(12)

        # Create the cipher with the nonce
        cipher = Cipher(
            algorithms.AES(self.current_session_keys['session_key']),
            modes.GCM(nonce),
            backend=self.backend
        )

        encryptor = cipher.encryptor()

        if is_file:
            with open(content, 'rb') as file:
                file_content = file.read()
            padded_content = file_content
        else:
            # If the content is a string, apply padding for AES encryption
            padder = sym_padding.PKCS7(128).padder()
            padded_content = padder.update(content.encode()) + padder.finalize()

        # Encrypt the padded content
        ciphertext = encryptor.update(padded_content) + encryptor.finalize()

        if is_file:
            encrypted_file_path = content + '.enc'
            with open(encrypted_file_path, 'wb') as file:
                file.write(ephemeral_public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
                file.write(nonce)
                file.write(encryptor.tag)
                file.write(ciphertext)
            return encrypted_file_path
        else:
            hmac = HMAC_PRIMITIVE(self.current_session_keys['session_key'], hashes.SHA256(), backend=self.backend)
            hmac.update(ciphertext)
            hmac_value = hmac.finalize()

            token = self.generate_replay_protection_token(content, recipient_identity_public_key)

            encrypted_content = {
                'ephemeral_public_key': ephemeral_public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).hex(),  # Convert ephemeral public key to hex
                'nonce': nonce.hex(),  # Convert nonce to hex
                'ciphertext': ciphertext.hex(),  # Convert ciphertext to hex
                'tag': encryptor.tag.hex(),  # Convert tag to hex
                'replay_token': token,  # Include the replay protection token
                'hmac': hmac_value.hex()  # Include the HMAC
            }
            return encrypted_content

    def decrypt(self, encrypted_content: dict, private_key: dh.DHPrivateKey, is_file: bool = False) -> str:
        """Decrypts a message or file content and ensures message integrity and freshness."""
        if is_file:
            with open(encrypted_content, 'rb') as file:
                ephemeral_public_key_bytes = file.read(800)  # Length of PEM encoded RSA public key
                nonce = file.read(12)
                tag = file.read(16)
                ciphertext = file.read()

            ephemeral_public_key = serialization.load_pem_public_key(
                ephemeral_public_key_bytes,
                backend=self.backend
            )
        else:
            ephemeral_public_key = serialization.load_pem_public_key(
                bytes.fromhex(encrypted_content['ephemeral_public_key']),
                backend=self.backend
            )
            nonce = bytes.fromhex(encrypted_content['nonce'])
            tag = bytes.fromhex(encrypted_content['tag'])
            ciphertext = bytes.fromhex(encrypted_content['ciphertext'])

        shared_key = private_key.exchange(
            ephemeral_public_key
        )

        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'session data',
            backend=self.backend
        ).derive(shared_key)

        cipher = Cipher(
            algorithms.AES(derived_key),
            modes.GCM(nonce, tag),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        decrypted_padded_content = decryptor.update(ciphertext) + decryptor.finalize()

        if is_file:
            decrypted_file_path = encrypted_content.replace('.enc', '')
            with open(decrypted_file_path, 'wb') as file:
                file.write(decrypted_padded_content)
            return decrypted_file_path
        else:
            unpadder = sym_padding.PKCS7(128).unpadder()
            decrypted_content = unpadder.update(decrypted_padded_content) + unpadder.finalize()

            token = encrypted_content['replay_token']
            if not self.verify_replay_protection_token(decrypted_content.decode(), token, private_key.public_key()):
                raise ValueError("Replay detected. The message has been replayed.")

            hmac = HMAC_PRIMITIVE(derived_key, hashes.SHA256(), backend=self.backend)
            hmac.update(ciphertext)
            hmac.verify(bytes.fromhex(encrypted_content['hmac']))

            return decrypted_content.decode() 

    def create_user_key_pair(self, password: str) -> tuple:
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

    def encrypt_user_private_key(self, private_key: rsa.RSAPrivateKey, key: bytes, salt: bytes) -> dict:
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

    def decrypt_user_private_key(self, encrypted_private_key: dict, password: str, salt: bytes) -> rsa.RSAPrivateKey:
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

    def hide_ip(self, message: str, ip_address: str) -> str:
        """Adds an IP hash to a message for privacy."""
        return f"{message} [IP: {hashlib.sha256(ip_address.encode()).hexdigest()}]"

    def verify_ip_hash(self, message: str, ip_hash: str, ip_address: str) -> bool:
        """Verifies the IP hash for the message."""
        return hashlib.sha256(ip_address.encode()).hexdigest() == ip_hash

    # Methods for socket integration
    def initiate_key_exchange(self) -> bytes:
        """Initiate key exchange and return the public key to be sent to the recipient."""
        return self.identity_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def receive_key_exchange(self, recipient_public_key_bytes: bytes) -> None:
        """Receive recipient's public key and rotate session keys."""
        recipient_public_key = serialization.load_pem_public_key(
            recipient_public_key_bytes,
            backend=self.backend
        )
        self.rotate_session_keys(recipient_public_key)

    def prepare_message(self, message: str, recipient_identity_public_key_bytes: bytes, recipient_signed_prekey_public_bytes: bytes, recipient_onetime_prekey_public_bytes: bytes) -> dict:
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

    def process_received_message(self, encrypted_content: dict) -> str:
        """Process a received encrypted message."""
        return self.decrypt(encrypted_content, self.identity_private_key)