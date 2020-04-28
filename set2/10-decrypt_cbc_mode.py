# Refernces:
# https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture8.pdf
# http://www.cs.columbia.edu/~sedwards/classes/2008/4840/reports/AES.pdf
# https://kavaliro.com/wp-content/uploads/2014/03/AES.pdf

import binascii
from base64_to_hex import base64_to_hex
from BitVector import *

rKey = []
forSBox = []
invSBox = []
rcon = [1, 0, 0, 0]

def getStateArray(block):
    state = [[0x0 for i in range(4)] for i in range(4)]
    for i in range(0, len(block), 2):
        p = int(block[i], 16)*16 + int(block[i+1], 16)
        c = i//8
        r = (i//2)%4
        state[r][c] = p
    return state

def genTable():
    AES_modulus = BitVector(bitstring='100011011')
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        forSBox.append(int(a))
        # For the decryption SBox
        b = BitVector(intVal = i, size=8)
        b1, b2, b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSBox.append(int(b))

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
    return res

def rangeXor(a, b):
    c = [0]*4
    for i in range(4):
        c[i] = (a[i] ^ b[i])
    return c

def printState(state):
    for i in range(4):
        for j in range(4):
            print(hex(state[i][j]), end=' ')
        print('\n')

def genRoundKeys(id):
    ckey = rKey[id+3]
    ckey = ckey[1:] + ckey[:1]
    for i in range(4):
        ckey[i] = forSBox[ckey[i]]
    ckey = rangeXor(ckey, rcon)
    for i in range(4):
        ckey = rangeXor(rKey[id+i], ckey)
        rKey.append(ckey)
    rcon[0] = gfmul2(rcon[0])
    
def genAllKeys(key):
    rc = []
    for i in range(len(key)):
        rc.append(ord(key[i]))
        if(len(rc) == 4):
            rKey.append(rc)
            rc = []
    for i in range(10):
        genRoundKeys(4*i)        
    
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
                newState[i][j] = newState[i][j] ^ fieldMultiply(state[k][j], mat[i][k])
    return newState

def invRoundKey(state, id):
    for i in range(4):
        for j in range(4):
            state[j][i] = (state[j][i] ^ rKey[id+i][j])
    return state

def invSubBytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = invSBox[state[i][j]]
    return state

def invStateArray(state):
    res = []
    for i in range(4):
        for j in range(4):
            res.append(state[j][i])
    res = bytearray(res)
    return res

def decrypt16bytes(data, key):

    data = getStateArray(data)

    # Inverse Round 10
    data = invRoundKey(data, 40)
    data = invShiftRows(data)
    data = invSubBytes(data)
   
    # Inverse Round 9-1
    for i in range(9, 0, -1):
        data = invRoundKey(data, i*4)
        data = invMixColumns(data)
        data = invShiftRows(data)
        data = invSubBytes(data)
    
    # Inverse Round 0
    data = invRoundKey(data, 0)
    data = invStateArray(data)

    return data

def decryptAES128CBC(cipher, key):

    genTable()
    
    ciphertext = base64_to_hex(cipher)

    genAllKeys(key)

    message = ""

    IV = bytearray(16)         # Initialisation Vector

    for i in range(0, len(ciphertext), 32):
        cipher = ciphertext[i:i+32]
        text = decrypt16bytes(cipher, key)
        text = [text[i]^IV[i] for i in range(len(text))]
        for element in text:
            message += chr(element)
        IV = [int(cipher[i:i+2], 16) for i in range(0, len(cipher), 2)]
        IV = bytearray(IV)

    return message

if __name__ == '__main__':
    
    with open('10.txt', 'r') as file:
        ciphertext = file.read().replace('\n','')  
   
    print(decryptAES128CBC(ciphertext, "YELLOW SUBMARINE"))

