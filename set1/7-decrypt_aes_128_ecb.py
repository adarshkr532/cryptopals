# https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture8.pdf


from base64_to_hex import base64_to_hex
from BitVector import *

def get_statearray(block):
    state = [[0x0 for i in range(4)] for i in range(4)]
    for i in range(0, len(block), 2):
        p = int(block[i], 16)*16 + int(block[i+1], 16)
        c = i//8
        r = (i//2)%4
        state[r][c] = p
    return state

def gen_table():
    AES_modulus = BitVector(bitstring='100011011')
    invSBox = []
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        b = BitVector(intVal = i, size=8)
        b1, b2, b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSBox.append(int(b))
    return invSBox

def invShiftRows(state):
    for i in range(4):
        for j in range(i):
            state[i] = state[i][3:] + state[i][:3]
    return state

def gfmul2(a):                  # Multiply by 2 in Galois Field
    res = (a << 1)
    res = (res & 255)
    if(a & 128):
        res = (res ^ 27)
    return res

def fieldMultiply(a, b):        # Multiply two numbers in Galois Field
    res = 0
    while(b > 0):
        if(b&1):
            res = (res ^ a)
        a = gfmul2(a)
        b = b//2
        print(a, b, res)
    return res


def invMixColumns(state):
    mat = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]
    newState = [[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                newState[i][j] = newState[i][j] ^ fieldMultiply(state[k][j], mat[i][k])
    return newState

#def decrypt_aes(s):


if __name__ == '__main__':
    
    with open('7.txt', 'r') as file:
        data = file.read().replace('\n','')
    
    data = base64_to_hex(data)

    state = get_statearray("8E4DA1BC9FDC589DD5D5D7D64D7EBDF8")
    
    for i in state:
        for j in i:
            print(hex(j), end = ' ')
        print('\n')

    state = invMixColumns(state)
    for i in state:
        for j in i:
            print(hex(j), end = ' ')
        print('\n')
