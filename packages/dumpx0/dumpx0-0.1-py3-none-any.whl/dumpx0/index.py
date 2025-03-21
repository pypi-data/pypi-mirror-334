import os
import socket
import struct
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Constants
AES_KEY_SIZE = 32  # AES-256
HMAC_KEY_SIZE = 32  # HMAC-256
IV_SIZE = 16  # IV size for AES-CBC


class X3DH:
    """Handles the X3DH Key Exchange securely."""

    @staticmethod
    def generate_keypair():
        """Generate an ECDH key pair for X3DH."""
        private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return private_key, public_key, private_pem, public_pem

    @staticmethod
    def derive_shared_secret_initiator(ik_sender, ek_sender, peer_ik, peer_spk, peer_opk=None):
        """
        X3DH key derivation for the initiator.
        - ik_sender: Initiator's identity key (private)
        - ek_sender: Initiator's ephemeral key (private)
        - peer_ik: Recipient's identity key (public)
        - peer_spk: Recipient's signed prekey (public)
        - peer_opk: Recipient's one-time prekey (optional)
        """
        shared_secret = (
            ik_sender.exchange(ec.ECDH(), peer_spk) +  # DH1
            ek_sender.exchange(ec.ECDH(), peer_ik) +  # DH2
            ek_sender.exchange(ec.ECDH(), peer_spk)   # DH3
        )
        
        if peer_opk:
            shared_secret += ek_sender.exchange(ec.ECDH(), peer_opk)  # DH4

        return HKDF(
            algorithm=hashes.SHA256(), length=32, salt=None, info=b"x3dh key exchange", backend=default_backend()
        ).derive(shared_secret)

    @staticmethod
    def derive_shared_secret_responder(spk_receiver, peer_ik, peer_ek, opk_receiver=None):
        """
        X3DH key derivation for the responder.
        - spk_receiver: Signed Prekey (private)
        - peer_ik: Initiator’s identity key (public)
        - peer_ek: Initiator’s ephemeral key (public)
        - opk_receiver: One-time prekey (private, if used)
        """
        shared_secret = (
            spk_receiver.exchange(ec.ECDH(), peer_ik) +  # DH1
            spk_receiver.exchange(ec.ECDH(), peer_ek) +  # DH3
            peer_ek.exchange(ec.ECDH(), spk_receiver.public_key())  # DH2
        )

        if opk_receiver:
            shared_secret += peer_ek.exchange(ec.ECDH(), opk_receiver.public_key())  # DH4

        return HKDF(
            algorithm=hashes.SHA256(), length=32, salt=None, info=b"x3dh key exchange", backend=default_backend()
        ).derive(shared_secret)


class Encryption:
    """Handles AES encryption and decryption with CBC mode."""

    @staticmethod
    def aes_256_cbc_encrypt(data, key):
        """Encrypt data using AES-256-CBC."""
        iv = os.urandom(IV_SIZE)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))
        return iv + ciphertext  # Prepend IV to ciphertext

    @staticmethod
    def aes_256_cbc_decrypt(data, key):
        """Decrypt AES-256-CBC encrypted data."""
        iv = data[:IV_SIZE]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(data[IV_SIZE:]), AES.block_size)
        return plaintext.decode("utf-8")


class HMAC:
    """Handles HMAC authentication."""

    @staticmethod
    def generate_hmac_sha256(key, message):
        """Generate an HMAC-SHA256 authentication tag."""
        h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(message)
        return h.finalize()

    @staticmethod
    def verify_hmac_sha256(key, message, mac):
        """Verify an HMAC-SHA256 authentication tag."""
        h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(message)
        h.verify(mac)  # Raises InvalidSignature if verification fails


class SecureSocket:
    """Handles secure socket communication with encryption and authentication."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Establish connection to the server."""
        self.socket.connect((self.host, self.port))

    def send_secure_message(self, message, aes_key, hmac_key):
        """Encrypt, authenticate, and send a message securely."""
        encrypted_message = Encryption.aes_256_cbc_encrypt(message, aes_key)
        message_mac = HMAC.generate_hmac_sha256(hmac_key, encrypted_message)

        # Send message length (4 bytes) + encrypted message + MAC
        msg_length = struct.pack("!I", len(encrypted_message))
        self.socket.sendall(msg_length + encrypted_message + message_mac)

    def receive_secure_message(self, aes_key, hmac_key):
        """Receive, decrypt, and authenticate a secure message."""
        msg_length_data = self._recv_exactly(4)
        msg_length = struct.unpack("!I", msg_length_data)[0]

        encrypted_message = self._recv_exactly(msg_length)
        received_mac = self._recv_exactly(HMAC_KEY_SIZE)

        # Verify and decrypt
        HMAC.verify_hmac_sha256(hmac_key, encrypted_message, received_mac)
        return Encryption.aes_256_cbc_decrypt(encrypted_message, aes_key)

    def _recv_exactly(self, num_bytes):
        """Helper function to receive exactly num_bytes from the socket."""
        data = b""
        while len(data) < num_bytes:
            packet = self.socket.recv(num_bytes - len(data))
            if not packet:
                raise ConnectionError("Connection lost while receiving data")
            data += packet
        return data

    def close(self):
        """Close the socket connection."""
        self.socket.close()
