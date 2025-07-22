import time

def left_shift(bits, shifts):
    """Left shift on a bit string in little-endian"""
    return bits[-shifts:] + bits[:-shifts]

def permute(bits, table):
    """Permutation to bit string using given table."""
    return ''.join(bits[i-1] for i in table)

def add_spaces(binary_str):
    """Space every 8 bits for readability."""
    return ' '.join(binary_str[i:i+8] for i in range(0, len(binary_str), 8))

# DES permutation tables
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Left shift schedule for each round
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def des_key_schedule(key):
    """DES key scheduling for a 64-bit key"""
    if len(key) != 64 or not all(bit in '01' for bit in key):
        raise ValueError("Key must be a 64-bit binary string")

    key = key[::-1]
    print("Input key (big-endian for display):", add_spaces(key[::-1]))

    pc1_key = permute(key, PC1)
    print("PC1 output:", add_spaces(pc1_key[::-1]))

    C = pc1_key[:28]
    D = pc1_key[28:]
    
    round_keys = []
    for round_num in range(16):
        print(f"\nRound {round_num + 1}:")
        print(f"C{round_num}:", add_spaces(C[::-1]))
        print(f"D{round_num}:", add_spaces(D[::-1]))
        
        shifts = SHIFT_SCHEDULE[round_num]
        C = left_shift(C, shifts)
        D = left_shift(D, shifts)
        
        print(f"Shifted C{round_num + 1}:", add_spaces(C[::-1]))
        print(f"Shifted D{round_num + 1}:", add_spaces(D[::-1]))
        
        CD = C + D
        print(f"Concatenated C{round_num + 1}D{round_num + 1}:", add_spaces(CD[::-1]))
        
        round_key = permute(CD, PC2)
        print(f"Round key {round_num + 1} (after PC2):", add_spaces(round_key[::-1]))
        round_key_hex = format(int(round_key[::-1], 2), '012x')
        print(f"Round key {round_num + 1} (hex):", round_key_hex)
        round_keys.append(round_key_hex)
    
    return round_keys

start = time.time()
key_input = "0000000100000001000000010000000100110001001100010011000100110001"
key_input = key_input.replace(" ","")
round_keys = des_key_schedule(key_input)
print(round_keys)
stop = time.time()
print(stop-start)
