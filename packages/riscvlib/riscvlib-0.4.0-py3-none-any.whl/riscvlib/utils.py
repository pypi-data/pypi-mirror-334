
ZERO_BYTES32 = b"\x00" * 32


def sign_extend_str(bit_str, target_length=32):
    """
    Sign extend bitstring
    :param bit_str: string
    :param target_length: int
    :return: string
    """
    original_length = len(bit_str)
    if original_length >= target_length:
        return bit_str  # No need to extend

    # Extract the most significant bit (MSB)
    msb = bit_str[0]

    # Repeat the MSB to fill the remaining bits
    extended_bits = msb * (target_length - original_length)
    return extended_bits + bit_str


def twos_complement_str(bit_str):
    """
    convert a bitstring -> 2's complement of bitstring
    :param bit_str: str - bitstring
    :return: str - 2's complement of input string
    """
    # if passed a leading '-', replace with a zero, it's a python format thing
    bit_str = bit_str.replace("-", "0", 1)
    bit_str = bit_str.replace('0b', "", 1)

    # Convert the bit string to an integer
    unsigned_value = int(bit_str, 2)
    bit_len = len(bit_str)

    # Calculate the 2's complement
    inverted_value = ~unsigned_value
    twos_complement_value = (inverted_value + 1) & ((1 << bit_len) - 1)

    # Convert back to a bit string
    twos_complement_string = format(twos_complement_value, f"0{bit_len}b")
    return twos_complement_string
