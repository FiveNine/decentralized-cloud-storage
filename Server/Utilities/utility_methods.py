def address_to_string(address: tuple[str, int]) -> str:
    return address[0] + ':' + str(address[1])

def string_to_address(string: str) -> tuple[str, int]:
    host, port = string.split(':')
    return host, int(port)