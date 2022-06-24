import os, io, json
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def save_keys(save_directory: str, save_name: str, key: bytes, signature: bytes, initialization_vector: bytes, tag: bytes):
    """
    Save key, signature, initialization vector and tag in a file.\n
    Arguments:
        save_directory: Directory to save the keys in.
        save_name: Name of the file to save the keys in (without extension).
        key: Encryption Key generated on Encryption.
        signature: Encryption Signature generated on Encryption.
        initialization_vector: Initialization vector generated on Encryption.
        tag: Tag generated on Encryption.
    """

    # Convert all bytes to base64 and then decode using utf-8 
    # to store them as strings in json
    key = b64encode(key).decode('utf-8')
    signature = b64encode(signature).decode('utf-8')
    initialization_vector = b64encode(initialization_vector).decode('utf-8')
    tag = b64encode(tag).decode('utf-8')

    key_object = {
        "Key": key,
        "Signature": signature,
        "IV": initialization_vector,
        "Tag": tag
    }
    
    file_name = save_name + ".key"
    with open(os.path.join(save_directory, file_name), 'w') as file:
        file.write(json.dumps(key_object, indent=4))

def get_keys(save_directory: str, save_name: str) -> tuple[bytes, bytes, bytes, bytes]:
    """
    Gets key, signature, initialization vector and tag stored in a file.\n
    Arguments:
        save_directory: Directory in which the save file is.
        save_name: Name of the file with the keys (without extension).
    Returns:
        key: Encryption Key generated on Encryption.
        signature: Encryption Signature generated on Encryption.
        initialization_vector: Initialization vector generated on Encryption.
        tag: Tag generated on Encryption.
    """

    file_name = save_name + ".key"

    with open(os.path.join(save_directory, file_name), 'r') as file:
        key_object = json.loads(file.read())

    key, signature, initialization_vector, tag = key_object.values()

    # Encode strings using utf-8 and use base64 decoding
    # to get the original values in bytes
    key = b64decode(key.encode('utf-8'))
    signature = b64decode(signature.encode('utf-8'))
    initialization_vector = b64decode(initialization_vector.encode('utf-8'))
    tag = b64decode(tag.encode('utf-8'))

    return (key, signature, initialization_vector, tag)

def iter_chunks(file: io.BytesIO, chunk_size: int = 64 * 1024):
    """Read chunks from a file"""
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data

class EncryptionIterator:
    """
    Encrypt a file iteratively
    Parameters
    ----------
    plaintext : io.BytesIO
        The file buffer to encrypt
    chunk_size : int
        How much data to encrypt per iteration
    Attributes
    ----------
    key : bytes
        The secret key for AES encryption
    signature : bytes
        Additional data used to verify the key for dec
    iv : bytes
        The 12-byte initialization vector for GCM. You will need this value for decryption.
    tag : bytes
        The tag to verfiy data integrity on decryption
    """

    def __init__(
        self,
        plaintext: io.BytesIO,
        chunk_size: int = 64 * 1024,
    ):
        self.key = os.urandom(32)
        self.signature = os.urandom(12)
        self.iv = os.urandom(12)
        self.file = plaintext
        self.chunk_size = chunk_size
        self.encryptor = Cipher(algorithms.AES(self.key), modes.GCM(self.iv)).encryptor()
        self.encryptor.authenticate_additional_data(self.signature)

    @property
    def tag(self):
        return self.encryptor.tag

    def __iter__(self):
        for chunk in iter_chunks(self.file, chunk_size=self.chunk_size):
            yield self.encryptor.update(chunk)

        yield self.encryptor.finalize()

class DecryptionIterator:
    """
    Decrypt a file iteratively
    Parameters
    ----------
    ciphertext : io.BytesIO
        The file buffer to decrypt
    key : bytes
        The secret key for AES decryption
    signature : bytes
        Additional data used to verify the key
    iv : bytes
        The initialization vector from the EncryptionIterator object
    tag : bytes
        The tag used for data integrity from the EncryptionIterator object
    chunk_size : int
        How much data to decrypt per iteration
    """

    def __init__(
        self,
        ciphertext: io.BytesIO,
        key: bytes,
        signature: bytes,
        iv: bytes,
        tag: bytes,
        chunk_size: int = 64 * 1024,
    ):
        self.iv = iv
        self.tag = tag
        self.file = ciphertext
        self.chunk_size = chunk_size
        self.decryptor = Cipher(
            algorithms.AES(key), modes.GCM(self.iv, self.tag)
        ).decryptor()
        self.decryptor.authenticate_additional_data(signature)

    def __iter__(self):
        for chunk in iter_chunks(self.file, chunk_size=self.chunk_size):
            yield self.decryptor.update(chunk)

        yield self.decryptor.finalize()
