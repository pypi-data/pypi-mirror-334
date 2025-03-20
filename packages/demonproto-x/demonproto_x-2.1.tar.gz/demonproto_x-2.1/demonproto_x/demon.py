import os
import secrets
import hashlib
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding, dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC as HMAC_PRIMITIVE

class demon:
    def __init__(self):
        self.backend = default_backend()

        # Generate Identity Key Pair (IK) using Diffie-Hellman for key exchange
        dh_parameters = dh.generate_parameters(generator=2, key_size=2048, backend=self.backend)
        self.identity_private_key = dh_parameters.generate_private_key()
        self.identity_public_key = self.identity_private_key.public_key()

        # Generate RSA-3072 Key Pair for digital signatures
        self.rsa_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=3072,
            backend=self.backend
        )
        self.rsa_public_key = self.rsa_private_key.public_key()

        self.current_session_keys = {}

        # Store previously seen replay protection tokens
        self.replay_protection_store = {}

    def generate_signed_prekey(self):
        # Generate Signed PreKey Pair (SPK) using Diffie-Hellman
        dh_parameters = dh.generate_parameters(generator=2, key_size=2048, backend=self.backend)
        self.signed_prekey_private = dh_parameters.generate_private_key()
        self.signed_prekey_public = self.signed_prekey_private.public_key()
        return self.signed_prekey_public

    def generate_onetime_prekey(self):
        # Generate One-Time PreKey Pair (OPK) using Diffie-Hellman
        dh_parameters = dh.generate_parameters(generator=2, key_size=2048, backend=self.backend)
        self.onetime_prekey_private = dh_parameters.generate_private_key()
        self.onetime_prekey_public = self.onetime_prekey_private.public_key()
        return self.onetime_prekey_public

    def sign_message(self, message):
        """Signs the message with the RSA-3072 private key."""
        signature = self.rsa_private_key.sign(
            message.encode(),
            rsa_padding.PSS(
                mgf=rsa_padding.MGF1(hashes.SHA256()),
                salt_length=rsa_padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, message, signature, public_key):
        """Verifies the signature using the RSA-3072 public key."""
        try:
            public_key.verify(
                signature,
                message.encode(),
                rsa_padding.PSS(
                    mgf=rsa_padding.MGF1(hashes.SHA256()),
                    salt_length=rsa_padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True  # Signature is valid
        except Exception:
            return False  # Signature is invalid

    def generate_shared_key(self, recipient_public_key):
    # Ensure the recipient public key is of the correct type
     if not isinstance(recipient_public_key, dh.DHPublicKey):
        raise ValueError("Recipient's public key must be a DHPublicKey.")

    # Generate shared key using Diffie-Hellman key exchange
     try:
        shared_key = self.identity_private_key.exchange(recipient_public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'session data',
            backend=self.backend
        ).derive(shared_key)
        return derived_key
     except ValueError as e:
        print(f"Error computing shared key: {e}")
        raise

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

    def encrypt(self, content, recipient_identity_public_key, recipient_signed_prekey_public, recipient_onetime_prekey_public, is_file=False):
        """Encrypts a message or file content for the recipient with forward secrecy."""
        shared_key = self.generate_shared_key(recipient_identity_public_key)

        # Additional payload fields
        length = 32  # 32-bit length
        payload_type = 32  # 32-bit payload type
        random_bytes = os.urandom(16)  # Minimum 128-bit random bytes
        layer = 32  # 32-bit layer
        in_seq_no = 32  # 32-bit incoming sequence number
        out_seq_no = 32  # 32-bit outgoing sequence number
        message_type = 32  # 32-bit message type
        serialized_message_object = content.encode() if not is_file else content
        padding_length = secrets.choice(range(12, 1025))  # Padding from 12 to 1024 bytes
        padding = os.urandom(padding_length)

        payload = (
            length.to_bytes(4, 'big') +
            payload_type.to_bytes(4, 'big') +
            random_bytes +
            layer.to_bytes(4, 'big') +
            in_seq_no.to_bytes(4, 'big') +
            out_seq_no.to_bytes(4, 'big') +
            message_type.to_bytes(4, 'big') +
            serialized_message_object +
            padding
        )

        # SHA-256 hash of the payload
        payload_hash = hashlib.sha256(payload).digest()

        # AES-256 GCM encryption
        key_fingerprint = hashlib.sha256(shared_key).digest()[:8]  # 64-bit key fingerprint
        iv = os.urandom(32)  # AES GCM IV 256-bit
        msg_key = hashlib.sha256(key_fingerprint + payload_hash).digest()  # KDF (SHA-256)

        cipher = Cipher(
            algorithms.AES(shared_key),
            modes.GCM(iv),
            backend=self.backend
        )

        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(payload) + encryptor.finalize()

        if is_file:
            encrypted_file_path = content + '.enc'
            with open(encrypted_file_path, 'wb') as file:
                file.write(recipient_identity_public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
                file.write(iv)
                file.write(encryptor.tag)
                file.write(ciphertext)
            return encrypted_file_path
        else:
            # Generate HMAC for message integrity
            hmac = HMAC_PRIMITIVE(shared_key, hashes.SHA256(), backend=self.backend)
            hmac.update(ciphertext)
            hmac_value = hmac.finalize()

            # Generate the replay protection token
            token = self.generate_replay_protection_token(content, recipient_identity_public_key)

            # Return serialized content with nonce, tag, ciphertext in hex, replay protection token, and HMAC
            encrypted_content = {
                'recipient_public_key': recipient_identity_public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).hex(),  # Convert recipient public key to hex
                'iv': iv.hex(),  # Convert IV to hex
                'ciphertext': ciphertext.hex(),  # Convert ciphertext to hex
                'tag': encryptor.tag.hex(),  # Convert tag to hex
                'replay_token': token,  # Include the replay protection token
                'hmac': hmac_value.hex()  # Include the HMAC
            }
            return encrypted_content

    def decrypt(self, encrypted_content, private_key, is_file=False):
        """Decrypts a message or file content and ensures message integrity and freshness."""
        if is_file:
            with open(encrypted_content, 'rb') as file:
                recipient_public_key_bytes = file.read(800)  # Length of PEM encoded RSA public key
                iv = file.read(32)
                tag = file.read(16)
                ciphertext = file.read()

            recipient_public_key = serialization.load_pem_public_key(
                recipient_public_key_bytes,
                backend=self.backend
            )
        else:
            recipient_public_key = serialization.load_pem_public_key(
                bytes.fromhex(encrypted_content['recipient_public_key']),
                backend=self.backend
            )
            iv = bytes.fromhex(encrypted_content['iv'])
            tag = bytes.fromhex(encrypted_content['tag'])
            ciphertext = bytes.fromhex(encrypted_content['ciphertext'])

        shared_key = self.generate_shared_key(recipient_public_key)

        cipher = Cipher(
            algorithms.AES(shared_key),
            modes.GCM(iv, tag),
            backend=self.backend
        )

        decryptor = cipher.decryptor()
        decrypted_payload = decryptor.update(ciphertext) + decryptor.finalize()

        # SHA-256 hash of the decrypted payload
        payload_hash = hashlib.sha256(decrypted_payload).digest()

        # Verify msg_key
        key_fingerprint = hashlib.sha256(shared_key).digest()[:8]  # 64-bit key fingerprint
        msg_key = hashlib.sha256(key_fingerprint + payload_hash).digest()

        if is_file:
            decrypted_file_path = encrypted_content.replace('.enc', '')
            with open(decrypted_file_path, 'wb') as file:
                file.write(decrypted_payload)
            return decrypted_file_path
        else:
            # Unpad the content if it's text
            unpadder = sym_padding.PKCS7(128).unpadder()
            decrypted_content = unpadder.update(decrypted_payload) + unpadder.finalize()

            # Verify the replay protection token
            token = encrypted_content['replay_token']
            if not self.verify_replay_protection_token(decrypted_content.decode(), token, recipient_public_key):
                raise Exception("Replay detected. The message has been replayed.")

            # Verify the HMAC
            hmac = HMAC_PRIMITIVE(shared_key, hashes.SHA256(), backend=self.backend)
            hmac.update(ciphertext)
            hmac.verify(bytes.fromhex(encrypted_content['hmac']))

            return decrypted_content.decode()  # Return decrypted content as text

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
        """Receive recipient's public key and generate shared key."""
        recipient_public_key = serialization.load_pem_public_key(
            recipient_public_key_bytes,
            backend=self.backend
        )
        shared_key = self.generate_shared_key(recipient_public_key)
        self.current_session_keys = {'session_key': shared_key}

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