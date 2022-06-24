import os, math
import Utilities.AES as AES

GIGA_BYTE = 1024 * 1024 * 1024
MEGA_BYTE = 1024 * 1024
KILO_BYTE = 1024

def divide_file(file_path: str) -> list[str]:
    """
    Encrypt the file using AES and divide it into 10 chunks.\n
    Arguments:
        file_path: Absolute path to the file to be divided.
    Return:
        List of paths to the encrypted and divided files.
    """
    file_path = os.path.abspath(file_path)
    identifier, extension = file_path.split('\\')[-1].split('.')
    file_size = os.path.getsize(file_path)

    # create temp folder to save encrypted files
    if not os.path.exists("./temp"):
        os.makedirs("./temp")

    # encrypt file
    plaintext_file = open(file_path, 'rb')
    encrypted_file_path = f"./temp/{identifier}.{extension}"
    encryptor = AES.EncryptionIterator(plaintext_file, min(math.ceil(file_size/4), 100 * MEGA_BYTE))
    print(encryptor.chunk_size)
    with open(encrypted_file_path, 'wb') as encrypted_file:
        for chunk in encryptor:
            encrypted_file.write(chunk)
    plaintext_file.close()

    # save encryption keys
    if not os.path.exists("./Keys"):
        os.makedirs("./Keys")
    AES.save_keys("./Keys", identifier, encryptor.key, encryptor.signature, encryptor.iv, encryptor.tag)

    # divide encrypted file
    total_size = os.path.getsize(encrypted_file_path)
    divisions = 10
    chunk_size = math.ceil(total_size / divisions)

    # Buffer size of chunk_size/4 allows smaller files 
    # to be divided evenly into 10 files. Tested for 
    # files greater than 2MB. Buffer size will be 100MB max.
    read_buffer = min(math.ceil(chunk_size/4), 100 * MEGA_BYTE)
    
    list_of_files: list[str] = []
    with open(encrypted_file_path, 'rb') as read_file:
        for i in range(0, divisions):
            with open(f'./temp/{identifier}{i}.{extension}', 'wb') as write_file:

                data_read_in_bytes = 0
                while True:
                    data = read_file.read(read_buffer)
                    if not data:
                        break

                    data_read_in_bytes += len(data)
                    write_file.write(data)
                    if data_read_in_bytes >= chunk_size:
                        break
                list_of_files.append(os.path.abspath(f'./temp/{identifier}{i}.{extension}'))
    
    return list_of_files

def restore_file(list_of_files: list[str]) -> str:
    identifier, extension = list_of_files[0].split('\\')[-1].split('.')
    identifier = identifier[0:-1]

    if not os.path.exists("./Downloads/temp"):
        os.makedirs("./Downloads/temp")

    merged_file_path = f'./Downloads/temp/{identifier}.{extension}'

    with open(merged_file_path, 'wb') as write_file:
        for file_path in list_of_files:
            with open(file_path, 'rb') as read_file:
                file_size = os.path.getsize(file_path)
                read_buffer = min(math.ceil(file_size/4), 100 * MEGA_BYTE)

                data_read = 0
                while True:
                    data = read_file.read(read_buffer)
                    if not data:
                        break
                    data_read += len(data)
                    write_file.write(data)
                    if data_read > file_size:
                        break
    
    decrypted_file_path = f"./Downloads/{identifier}.{extension}"
    ciphertext_file_size = os.path.getsize(merged_file_path)
    ciphertext_file = open(merged_file_path, 'rb')

    key, signature, iv, tag = AES.get_keys("./Keys", identifier)
    decryptor = AES.DecryptionIterator(
        ciphertext= ciphertext_file,
        key= key,
        signature= signature,
        iv= iv,
        tag= tag,
        chunk_size= min(math.ceil(ciphertext_file_size/4), 100 * MEGA_BYTE)
    )
    print(decryptor.chunk_size)
    with open(decrypted_file_path, 'wb') as decrypted_file:
        for chunk in decryptor:
            decrypted_file.write(chunk)
    ciphertext_file.close()
    
    delete_directory("./Downloads/temp/")

    return decrypted_file_path

def delete_directory(path: str) -> None:
    for file_name in os.listdir(path):
        file = path + file_name
        if os.path.isfile(file):
            os.unlink(file)
        elif os.path.isdir(file):
            delete_directory(file)
    os.rmdir(path)

def address_to_string(address: tuple[str, int]) -> str:
    return address[0] + ':' + str(address[1])

def string_to_address(string: str) -> tuple[str, int]:
    host, port = string.split(':')
    return host, int(port)
