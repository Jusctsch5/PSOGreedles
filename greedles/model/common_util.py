def binary_array_to_int(arr):
    result = 0
    for val in arr:
        result = (result << 8) | val
    return result


def binary_array_to_hex(arr):
    return "".join(f"{x:02X}" for x in arr)


def string_to_char_codes(string):
    char_codes = ""
    for char in string:
        code = ord(char)
        front = (code & 0xFF00) >> 8
        back = code & 0x00FF
        char_codes += f"{back:02x}{front:02x}"
    return char_codes.upper()


def int_to_hex(value):
    return f"0x{value:06X}"
