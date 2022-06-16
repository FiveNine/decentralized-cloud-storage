import os, math
import Utilities.AES as AES

def divide_file(full_path: str) -> list[str]:
    full_path = os.path.abspath(full_path)
    identifier, extension = full_path.split('\\')[-1].split('.')

    key = AES.generate_key(identifier)
    encrypted_file_path = AES.encrypt_file(full_path, key)

    total_size = os.path.getsize(encrypted_file_path) # in bytes
    divisions = 10
    chunk_size = math.ceil(total_size / divisions)
    prev_pos = 0
    
    for i in range(0, divisions):
        with open(encrypted_file_path, 'rb') as read_file, open(f'./temp/{identifier}{i}.{extension}', 'wb') as write_file:
            data_read_in_bytes = 0

            # Buffer size of chunk_size/4 allows smaller files 
            # to be divided evenly into 10 files. Tested for 
            # files greater than 2MB. Buffer size will be 100MB max.
            read_buffer = min(math.ceil(chunk_size/4), 100 * 1024 * 1024)
            read_file.seek(prev_pos)

            while True:
                data = read_file.read(read_buffer)
                if not data:
                    prev_pos = read_file.tell()
                    break

                data_read_in_bytes += len(data)
                write_file.write(data)
                if data_read_in_bytes > chunk_size:
                    prev_pos = read_file.tell()
                    break
    
    return os.listdir('./temp/')

def delete_directory(path: str) -> None:
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                delete_directory(file_path)
                os.rmdir(file_path)
        except Exception as e:
            print(e)

def address_to_string(address: tuple[str, int]) -> str:
    return address[0] + ':' + str(address[1])

def string_to_address(string: str) -> tuple[str, int]:
    host, port = string.split(':')
    return host, int(port)

# def merge_files()

