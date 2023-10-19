from PIL import Image
import base64


def color_to_bits(color, color_map):
    return color_map[color]


def extract_data_from_image(img, color_map):
    width, height = img.size
    binary_data = ""

    for i in range(width):
        for j in range(height):
            pixel = img.getpixel((i, j))
            binary_data += color_to_bits(pixel, color_map)

    return binary_data


def binary_to_ascii(binary_data):
    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i : i + 8]
        chars.append(chr(int(byte, 2)))
    return "".join(chars)


def binary_to_hex(binary_data):
    hex_data = hex(int(binary_data, 2))[2:]
    return hex_data


def binary_to_decimal(binary_data):
    decimal_data = int(binary_data, 2)
    return decimal_data


def search_for_pattern(data, pattern="SKY-"):
    # Search in Binary
    if pattern in binary_to_ascii(data):
        return True, "Binary to ASCII"

    # Search in Hexadecimal
    hex_data = binary_to_hex(data)
    if pattern in bytes.fromhex(hex_data).decode("utf-8", errors="ignore"):
        return True, "Binary to Hexadecimal"

    # Search in Base64
    base64_data = binary_to_base64(data)
    if pattern in base64.b64decode(base64_data).decode("utf-8", errors="ignore"):
        return True, "Binary to Base64"

    return False, ""


def binary_to_base64(binary_data):
    n = int(binary_data, 2)
    byte_array = bytearray()
    while n:
        byte_array.append(n & 0xFF)
        n >>= 8
    byte_array.reverse()
    base64_data = base64.b64encode(byte_array).decode("utf-8")
    return base64_data


if __name__ == "__main__":
    image_path = "C:\\Users\\mikec\\Downloads\\code.png"  # Replace with your image path
    img = Image.open(image_path)

    colors = [
        (0, 0, 0, 255),
        (255, 255, 255, 255),
        (0, 255, 255, 255),
        (255, 0, 255, 255),
        (255, 0, 0, 255),
        (0, 0, 255, 255),
        (0, 255, 0, 255),
        (255, 255, 0, 255),
    ]

    color_map = {color: bin(i)[2:].zfill(3) for i, color in enumerate(colors)}

    binary_data = extract_data_from_image(img, color_map)
    ascii_data = binary_to_ascii(binary_data)
    hex_data = binary_to_hex(binary_data)
    decimal_data = binary_to_decimal(binary_data)
    base64_data = binary_to_base64(binary_data)

    # print(f"Binary: {binary_data}")
    # print(f"ASCII: {ascii_data}")
    # print(f"Hexadecimal: {hex_data}")
    # print(f"Base64: {base64_data}")
    found, method = search_for_pattern(binary_data, "SKY-")
    if found:
        print(f"'SKY-' found using conversion: {method}")
    else:
        print("Pattern 'SKY-' not found in the outputs.")
