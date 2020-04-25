import binascii
from base64_to_hex import base64_to_hex
from detect import detect_single_xor 

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

def get_keysize(data):
    l = []
    for keysize in range(2, 41):
        s = data[0:keysize*2]
        t = data[keysize*2:keysize*4]
        dis = hamming_distance(s, t)
        dis = (1.0*dis)/keysize
        l.append(tuple((dis, keysize)))
    l.sort()
    return l[:3]

def get_key(data, keysize):           #keysize is in bytes
    block = [""]*int(keysize)
    for i in range(len(data)):
        block[i%keysize] += data[i]
    key = ""
    for i in range(keysize):
        key += chr(detect_single_xor(block[i])[1])
    return key

if __name__ == '__main__':
    
    with open('6.txt', 'r') as file:
        data = file.read().replace('\n', '')
    data = base64_to_hex(data)
    
    keysize = get_keysize(data)

    for sz in keysize:
        key = get_key(data, sz[1])
        print(keysize, key)
