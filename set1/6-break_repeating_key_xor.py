import binascii
from base64_to_hex import base64_to_hex
from detect import detect_single_xor 
from repeat import repeating_key_xor

def to_hex(s):
    try:
        int(s, 16)
        return s
    except ValueError:
        return s.encode().hex()

def hamming_distance(s, t):
    dis = 0
    s = to_hex(s)
    t = to_hex(t)
    for i in range(0, len(s)):
        p = int(s[i], 16)^int(t[i], 16)
        dis += bin(p).count('1')
    return dis

def score(data, keysize):
    k = 2*keysize
    n = len(data)//k - 1
    total = 0
    for i in range(n):
        s = data[i*k: i*k + k]
        t = data[i*k + k: i*k + 2*k]
        total += hamming_distance(s, t)
    total = (total/keysize)/n
    return total

def get_keysize(data):
    l = []
    mn = 1000000
    for sz in range(2, 40):
        val = score(data, sz)
        if(val < mn):
            mn = val
            keysize = sz
    return keysize

def get_key(data, keysize):         # keysize in bytes 
    block = [""]*int(keysize)
    for i in range(0, len(data), 2):
        id = (i//2)%keysize
        block[id] += data[i]
        block[id] += data[i+1]
    key = ""
    for i in range(keysize):
        key += chr(detect_single_xor(block[i])[1])
    return key

if __name__ == '__main__':
    
    with open('6.txt', 'r') as file:
        data = file.read().replace('\n', '')
    
    data = base64_to_hex(data)
    
    keysize = get_keysize(data)

    key = get_key(data, keysize)

    print('Key: ', key, '\n')

    msg = repeating_key_xor(data, key)
    msg = binascii.unhexlify(msg)
    msg = str(msg, 'ascii')
    print ('Message:\n', msg)
