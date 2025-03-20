import os
import secrets
import base64
import hashlib
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ed25519, x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC as HMAC_PRIMITIVE
import json

class E2EEChatProtocol:
    def __init__(self):
        self.backend = default_backend()

        # Generate RSA private/public key for long-term identity and ECC keys
        self.ed25519_private_key = ed25519.Ed25519PrivateKey.generate()
        self.ed25519_public_key = self.ed25519_private_key.public_key()

        self.x25519_private_key = x25519.X25519PrivateKey.generate()
        self.x25519_public_key = self.x25519_private_key.public_key()

        self.current_session_keys = {}

        # Store previously seen replay protection tokens
        self.replay_protection_store = {}

    def generate_ephemeral_key_pair(self):
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        return private_key, public_key

    def rotate_session_keys(self, recipient_public_key):
        recipient_public_key = x25519.X25519PublicKey.from_public_bytes(recipient_public_key)
        
        ephemeral_private_key, ephemeral_public_key = self.generate_ephemeral_key_pair()
        shared_key = ephemeral_private_key.exchange(recipient_public_key)

        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'session data',
            backend=self.backend
        ).derive(shared_key)

        self.current_session_keys = {
            'ephemeral_private_key': ephemeral_private_key,
            'ephemeral_public_key': ephemeral_public_key,
            'derived_key': derived_key
        }

        return ephemeral_public_key

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
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()
        
        if recipient_key not in self.replay_protection_store:
            self.replay_protection_store[recipient_key] = []

        self.replay_protection_store[recipient_key].append(token)

        return token

    def verify_replay_protection_token(self, message, token, recipient_public_key):
        """Verifies if a message has been replayed using the stored token data."""
        recipient_key = recipient_public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()

        stored_tokens = self.replay_protection_store.get(recipient_key, [])

        message_hash = hashlib.sha256(message.encode()).hexdigest()

        for stored_token in stored_tokens:
            if stored_token['message_hash'] == message_hash and stored_token['nonce'] == token['nonce']:
                # If we find the same message hash with the same nonce, this is a replay
                return False

        # If token is not found or the nonce is different, this message is new
        return True

    def encrypt(self, content, metadata, recipient_public_key):
        """Encrypts a message or file content with metadata for the recipient with forward secrecy."""
        ephemeral_public_key = self.rotate_session_keys(recipient_public_key)

        # Generate a nonce (IV) for GCM mode
        nonce = os.urandom(12)

        # Prepare metadata for encryption
        metadata_json = json.dumps(metadata).encode('utf-8')
        
        # Combine content and metadata into one byte stream (metadata first, followed by content)
        combined_content = metadata_json + b"\n" + content

        # Create the cipher with the nonce
        cipher = Cipher(
            algorithms.AES(self.current_session_keys['derived_key']),
            modes.GCM(nonce),
            backend=self.backend
        )

        encryptor = cipher.encryptor()

        # If the content is a string, apply padding for AES encryption
        if isinstance(content, str):  # Treat it as text content if it's a string
            padder = sym_padding.PKCS7(128).padder()
            padded_content = padder.update(combined_content) + padder.finalize()
        else:  # If it's binary data (like a file), we don't need padding
            padded_content = combined_content

        # Encrypt the padded content
        ciphertext = encryptor.update(padded_content) + encryptor.finalize()

        # Generate the replay protection token
        token = self.generate_replay_protection_token(content, recipient_public_key)

        # Generate a real signature for the content
        signature = self.sign_message(content)

        # Return serialized content with nonce, tag, ciphertext in hex, replay protection token, and signature
        encrypted_content = {
            'ephemeral_public_key': ephemeral_public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            ).hex(),  # Convert ephemeral public key to hex
            'nonce': nonce.hex(),  # Convert nonce to hex
            'ciphertext': ciphertext.hex(),  # Convert ciphertext to hex
            'tag': encryptor.tag.hex(),  # Convert tag to hex
            'replay_token': token,  # Include the replay protection token
            'signature': signature.hex()  # Include the signature
        }

        return encrypted_content

    def decrypt(self, encrypted_content, private_key):
        """Decrypts a message or file content along with metadata and ensures message integrity and freshness."""
        ephemeral_public_key = x25519.X25519PublicKey.from_public_bytes(
            bytes.fromhex(encrypted_content['ephemeral_public_key'])
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
                bytes.fromhex(encrypted_content['nonce']),
                bytes.fromhex(encrypted_content['tag'])
            ),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        decrypted_padded_content = decryptor.update(bytes.fromhex(encrypted_content['ciphertext'])) + decryptor.finalize()

        # Unpad the content if it's text (for file, we don't need unpadding)
        try:
            unpadder = sym_padding.PKCS7(128).unpadder()
            decrypted_content = unpadder.update(decrypted_padded_content) + unpadder.finalize()

            # Split the decrypted content back into metadata and actual content
            metadata_json, file_content = decrypted_content.split(b"\n", 1)
            metadata = json.loads(metadata_json.decode('utf-8'))
            
            # Verify the replay protection token
            token = encrypted_content['replay_token']
            if not self.verify_replay_protection_token(file_content.decode(), token, private_key.public_key()):
                raise Exception("Replay detected. The message has been replayed.")

            # Verify the signature
            signature = bytes.fromhex(encrypted_content['signature'])
            if not self.verify_signature(file_content.decode(), signature, self.ed25519_public_key):
                raise Exception("Signature verification failed. The message may have been tampered with.")
            
            return metadata, file_content.decode()  # Return metadata and decrypted content as text
        except ValueError:
            # If unpadding fails, treat as binary file content
            metadata_json, file_content = decrypted_padded_content.split(b"\n", 1)
            metadata = json.loads(metadata_json.decode('utf-8'))
            
            # Verify the replay protection token
            token = encrypted_content['replay_token']
            if not self.verify_replay_protection_token(file_content, token, private_key.public_key()):
                raise Exception("Replay detected. The message has been replayed.")

            # Verify the signature
            signature = bytes.fromhex(encrypted_content['signature'])
            if not self.verify_signature(file_content, signature, self.ed25519_public_key):
                raise Exception("Signature verification failed. The message may have been tampered with.")
            
            return metadata, file_content  # Return metadata and binary content

    def sign_message(self, message):
        """Signs a message with Ed25519 to ensure authenticity."""
        return self.ed25519_private_key.sign(message.encode())

    def verify_signature(self, message, signature, public_key):
        """Verifies the authenticity of a message using Ed25519."""
        try:
            public_key.verify(signature, message.encode())
            return True
        except:
            return False

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
        return x25519.X25519PrivateKey.from_private_bytes(private_key_bytes)

    def hide_ip(self, message, ip_address):
        """Adds an IP hash to a message for privacy."""
        return f"{message} [IP: {hashlib.sha256(ip_address.encode()).hexdigest()}]"

    def verify_ip_hash(self, message, ip_hash, ip_address):
        """Verifies the IP hash for the message."""
        return hashlib.sha256(ip_address.encode()).hexdigest() == ip_hash

    # Methods for socket integration
    def initiate_key_exchange(self):
        """Initiate key exchange and return the public key to be sent to the recipient."""
        return self.x25519_public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    def receive_key_exchange(self, recipient_public_key_bytes):
        """Receive recipient's public key and rotate session keys."""
        recipient_public_key = x25519.X25519PublicKey.from_public_bytes(recipient_public_key_bytes)
        self.rotate_session_keys(recipient_public_key)

    def prepare_message(self, message, metadata, recipient_public_key_bytes):
        """Prepare an encrypted message for sending via socket."""
        recipient_public_key = x25519.X25519PublicKey.from_public_bytes(recipient_public_key_bytes)
        return self.encrypt(message, metadata, recipient_public_key)

    def process_received_message(self, encrypted_content):
        """Process a received encrypted message."""
        return self.decrypt(encrypted_content, self.x25519_private_key)

    def sign_for_authentication(self, message):
        """Sign a message for authentication purposes."""
        return self.sign_message(message)

    def verify_authentication(self, message, signature, public_key_bytes):
        """Verify the authenticity of a signed message."""
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
        return self.verify_signature(message, signature, public_key)