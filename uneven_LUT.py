# bi = xi - max(xj)
# bi is a fixed point number with 3 integer bits and 6 fraction bits (no sign bit since bi is always negative).
# For simplicity, bi is represented as a 9-bit integers in this Python program.
# LUT stores 2^(bi) with a fixed point number with 0 integer bit and 6 fraction bits.
# For simplicity, 2^(bi) is represented as a 6-bit integer in this Python program.

LUT = [
    # bucket 0
    [
        0b111111,
        0b111110,
        0b111110,
        0b111101,
        0b111100,
        0b111100,
        0b111011,
        0b111010,
    ],
    # bucket 1
    [
        0b111010,
        0b111001,
        0b111001,
        0b111000,
        0b110111,
        0b110111,
        0b110110,
        0b110110,
    ],
    # bucket 2
    [
        0b110101,
        0b110100,
        0b110011,
        0b110010,
        0b110001,
        0b110000,
        0b101111,
        0b101110,
    ],
    # bucket 3
    [
        0b101101,
        0b101011,
        0b101001,
        0b100111,
        0b100101,
        0b100100,
        0b100010,
        0b100001,
    ],
    # bucket 4
    [
        0b100000,
        0b011101,
        0b011010,
        0b011000,
        0b010110,
        0b010100,
        0b010011,
        0b010001,
    ],
    # bucket 5
    [
        0b010000,
        0b001101,
        0b001011,
        0b001001,
        0b001000,
        0b000111,
        0b000110,
        0b000101,
    ],
    # bucket 6
    [
        0b000100,
        0b000011,
        0b000010,
        0b000001,
        0b000001,
        0b000001,
        0b000000,
        0b000000,
    ],
]

def uneven_lut_index(bi):
    """
    Given bi as the format described above (fixed point number represented as 9-bit integers),
    return the bucket number and index into the LUT

    :param value: bi
    :return: [bucket number, index in the bucket]
    """
    if bi >> 3 == 0:
        return (0, bi)
    if bi >> 3 == 1:
        return (1, bi & 0b111)
    if bi >> 4 == 1:
        return (2, (bi >> 1) & 0b111)
    if bi >> 5 == 1:
        return (3, (bi >> 2) & 0b111)
    if bi >> 6 == 1:
        return (4, (bi >> 3) & 0b111)
    if bi >> 7 == 1:
        return (5, (bi >> 4) & 0b111)
    if bi >> 8 == 1:
        return (6, (bi >> 5) & 0b111)
    return 

if __name__ == '__main__':
    '''
    An example: bi represented as 0b000111111
    Integer bits are 000
    Fraction bits are 111111
    Thus, bi is -63/64 in fraction format (negative sign inherently added by processor)

    2^bi (based on the LUT) is represented as 0b100001
    Fraction bits are 100001
    Thus, 2^bi is 33/64 in fraction format
    '''
    bi = 0b000111111
    LUT_indices = uneven_lut_index(bi)
    print(LUT_indices)
    print(bin(LUT[LUT_indices[0]][LUT_indices[1]]))