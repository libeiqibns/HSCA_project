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
    return (6, 0b111)

import math

N = 10  # For our case. We can later check for higher N values
NUMLEVELS = math.ceil(math.log2(N))

# Objective: To compute numerator/D

# First need to normalize D
# 0.5<= normalized_D <1
# Establish a LUT for the Left Shift/Scaling Bits (Comparator based) (ceil(log2(N)) number of comparator levels and Scaling LUT size)

# D is from 1 to N
# if D is 1, numerator is our answer directly
# Else:
# First right shift D by ceil(log2(N)) bits to form scaledDownD
# Now look up the Scaling LUT to left shift scaledDownD to form normalized_D
# Now apply Newton Raphson to find 1/normalized_D
# Now use the same scaling factor for the numerator and then multiply this 1/normalized_D by normalized_numerator

def searchScalingLUT(scaledDownD):
    leftShiftBits = 0
    if scaledDownD == 1:
        return 0
    """    while scaledDownD < 1:
        scaledDownD = scaledDownD * 2.0
        leftShiftBits = leftShiftBits + 1
    return leftShiftBits
    """

    if scaledDownD <= (2**-3) and scaledDownD > (2**-4):
        leftShiftBits = 3
    if scaledDownD <= (2**-2) and scaledDownD > (2**-3):
        leftShiftBits = 2
    if scaledDownD < (2**-1) and scaledDownD > (2**-2):
        leftShiftBits = 1
    if scaledDownD <= (2**0) and scaledDownD >= (2**-1):
        leftShiftBits = 0
    return leftShiftBits
    """
    # Implement using For Loop (Comparator-based)
    leftShiftBits = NUMLEVELS - 1
    lowerLimit = 2 ** (-NUMLEVELS)
    for i in range(NUMLEVELS):
        if scaledDownD > lowerLimit and scaledDownD <= 2 * lowerLimit:
            return leftShiftBits
        else:
            leftShiftBits = leftShiftBits - 1
            lowerLimit = lowerLimit * 2
    """


# returns normalized D and the required effective right scaling bits
def NormalizeD(D):
    if D == 1:
        return 1, 0
    else:
        rightShiftBits = (
            NUMLEVELS  # Also = number of comparator levels and Scaling LUT size
        )
        # scaledDownD = D >> rightShiftBits  # fixed point right shift
        scaledDownD = D / (2**rightShiftBits)
        # print(scaledDownD)
        leftShiftBits = searchScalingLUT(scaledDownD)
        # print(leftShiftBits)
        # normalized_D = scaledDownD << leftShiftBits
        normalized_D = scaledDownD * (2**leftShiftBits)
        effectiveRightScalingBits = rightShiftBits - leftShiftBits
        return normalized_D, effectiveRightScalingBits


def NewtonRaphson(numerator, D):
    normalized_D, effectiveRightScalingBits = NormalizeD(D)
    # print(normalized_D)
    # print(effectiveRightScalingBits)
    normalized_numerator = numerator / (2**effectiveRightScalingBits)
    # numerator >> effectiveRightScalingBits
    # So that same scaling for numerator and denominator
    # Now compute 1/normalized_D and then multiply with normalized_numerator
    if normalized_D == 1:
        return normalized_numerator
    iterations = 3
    X0 = 2.914 - 2 * normalized_D
    Xi = X0
    while iterations:
        Xi_plus_1 = Xi * (2 - normalized_D * Xi)
        Xi = Xi_plus_1
        iterations = iterations - 1
    oneByNormD = Xi
    finalResult = oneByNormD * normalized_numerator
    return finalResult


def convert_num_to_9f(bi):
    '''
    Converts a number into the 9-bit fixed point format described at the top.
    For debugging purpose only
    
    :param value: bi in Python floating point format
    :return: bi in 9-bit fixed point format
    '''
    int_part = int(bi)
    frac_part = bi - int_part
    return int(int_part << 6 + int(frac_part * 64))

def convert_6f_to_num(e):
    '''
    Converts a 6-bit fixed point number (data stored in LUT) into a regular floating point number.
    For debugging purpose only
    
    :param value: e in 6-bit fixed point number format decribed above
    :return: e in Python floating point format
    '''
    return e / 64

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
    # bi = 0b000111111
    # LUT_indices = uneven_lut_index(bi)
    # print(LUT_indices)
    # print(bin(LUT[LUT_indices[0]][LUT_indices[1]]))

    '''
    An example: softmax([0,1,2,3,4,5,6,7,8])
    '''
    z = [0,1,2,3,4,5,6,7,8]
    # preprocess data: bi = zi - max(zj)
    max_z = max(z)
    b = [convert_num_to_9f(abs(zi - max_z)) for zi in z]
    LUT_indices = [uneven_lut_index(bi) for bi in b]
    e = [convert_6f_to_num(LUT[ind[0]][ind[1]]) for ind in LUT_indices]
    sum_e = sum(e)
    softmax = [NewtonRaphson(ei, sum_e) for ei in e]

    golden_e = [2 ** zi for zi in z]
    sum_golden_e = sum(golden_e)
    golden_softmax = [golden_ei / sum_golden_e for golden_ei in golden_e]

    print('Our Softmax: ',softmax)
    print('Ground Truth Softmax: ', golden_softmax)