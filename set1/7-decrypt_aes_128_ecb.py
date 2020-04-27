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

def invMixColumns(state):
    mat = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]
    newState = [[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                newState[i][j] = newState[i][j] ^ (mat[i][k] * state[k][j])
    return newState

#def decrypt_aes(s):


if __name__ == '__main__':
    
    with open('7.txt', 'r') as file:
        data = file.read().replace('\n','')
    
    data = base64_to_hex(data)

    state = get_statearray("29C3505F571420F6402299B31A02D73A")
    
    for i in state:
        for j in i:
            print(hex(j), end = ' ')
        print('\n')
    state = invMixColumns(state)
    for i in state:
        for j in i:
            print(hex(j), end = ' ')
        print('\n')
