from cryptography.fernet import Fernet
import os

def generate_key(file_name: str) -> bytes:
    key = Fernet.generate_key()
    if not os.path.exists("./Keys"):
        os.makedirs("./Keys")
    with open(f"./Keys/{file_name}.key", 'wb') as key_file:
        key_file.write(key)
    return key

def get_key(file_name: str) -> None:
    try:
        return open(f"./Keys/{file_name}.key", 'rb').read()
    except FileNotFoundError:
        print("Key file not found in Keys directory.")

def encrypt_file(file_path: str, key: bytes) -> str:
    file_path = os.path.abspath(file_path)
    identifier, extension = file_path.split('\\')[-1].split('.')

    if not os.path.exists("./Encrypted"):
        os.makedirs("./Encrypted")

    with open(file_path, 'rb') as file_to_encrypt, open(f"./temp/{identifier}.{extension}", 'wb') as encrypted_file:
        f = Fernet(key)
        read_buffer = 50 * 1024 * 1024 # 50MB

        while True:
            data = file_to_encrypt.read(read_buffer)
            if not data:
                break
            encrypted_data = f.encrypt(data)
            encrypted_file.write(encrypted_data)
    return f"./temp/{identifier}.encrypted"

def decrypt_file(file_path: str, key: bytes) -> None:
    file_path = os.path.abspath(file_path)
    identifier, extension = file_path.split('\\')[-1].split('.')

    if not os.path.exists("./Decrypted"):
        os.makedirs("./Decrypted")

    with open(file_path, 'rb') as file_to_decrypt, open(f"./Decrypted/{identifier}.{extension}", 'wb') as decrypted_file:
        f = Fernet(key)
        read_buffer = 50 * 1024 * 1024 # 50MB

        while True:
            data = file_to_decrypt.read(read_buffer)
            if not data:
                break
            decrypted_data = f.decrypt(data)
            decrypted_file.write(decrypted_data)
    
# ----test----
# generate_key("./test.file")
# print("Key Generated")

# key = get_key("./test.file")
# print(key)

# encrypt_file("./test.file", key)
# print("File Encrypted")

# decrypt_file("./Encrypted/test.file", key)
# print("File Decrypted")