import itertools
import re
import string
import struct


def generate_pattern(length: int) -> str:
    """Generate a cyclic pattern."""
    return "".join(
        "".join(triplet)
        for triplet in itertools.islice(
            itertools.product(
                string.ascii_uppercase, string.ascii_lowercase, string.digits
            ),
            length // 3 + 1,
        )
    )[:length]


def find_offset(value: str, length: int) -> list[int]:
    """Find the offset of a value inside a cyclic pattern."""
    pattern = generate_pattern(length)

    if value.startswith("0x"):
        hex_length = len(value) - 2
        hex_packing_map = {4: "<H", 8: "<I", 16: "<Q"}
        if hex_length not in hex_packing_map:
            raise ValueError(
                "Hex value must be exactly 4, 8, or 16 hex digits (2, 4, or 8 bytes)."
            )
        try:
            value_bytes = struct.pack(hex_packing_map[hex_length], int(value, 16))
        except ValueError:
            raise ValueError(f"Invalid hexadecimal input: {value}.")
    elif len(value) in (2, 4, 8):
        value_bytes = value.encode()
    else:
        raise ValueError(
            "Input must be a 2-character, 4-character, or 8-character string or hexadecimal equivalent."
        )

    return [m.start() for m in re.finditer(re.escape(value_bytes.decode()), pattern)]
