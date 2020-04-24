import binascii

# From http://www.data-compression.com/english.html
freqs = {
    'a': 0.0651738,
    'b': 0.0124248,
    'c': 0.0217339,
    'd': 0.0349835,
    'e': 0.1041442,
    'f': 0.0197881,
    'g': 0.0158610,
    'h': 0.0492888,
    'i': 0.0558094,
    'j': 0.0009033,
    'k': 0.0050529,
    'l': 0.0331490,
    'm': 0.0202124,
    'n': 0.0564513,
    'o': 0.0596302,
    'p': 0.0137645,
    'q': 0.0008606,
    'r': 0.0497563,
    's': 0.0515760,
    't': 0.0729357,
    'u': 0.0225134,
    'v': 0.0082903,
    'w': 0.0171272,
    'x': 0.0013692,
    'y': 0.0145984,
    'z': 0.0007836,
    ' ': 0.1918182 
}

def score(s):
    score = 0
    for i in s:
        c = chr(i).lower()
        if c in freqs:
            score += freqs[c]
    return score

def detect_single_xor(data):
    hexkey = "0123456789abcdef"
    res = ""
    mx = 0
    for s in data.split('\n'):
        for i in range (256):
            ht = ""
            count = 0
            for j in range(0, len(s), 2):
                c1 = int(s[j], 16)
                if(j+1 >= len(s)):
                    c2 = 0
                else:
                    c2 = int(s[j+1], 16)
                c = c1*16 + c2
                c = c^i
                ht += hexkey[c//16] + hexkey[c%16]
            ht = binascii.unhexlify(ht)
            if(score(ht) > mx):
                mx = score(ht)
                res = ht
                key = i
    return (res, key)

if __name__ == '__main__':
    with open('4.txt', 'r') as file:
        data = file.read()
    res = detect_single_xor(data)
    print ('Message:', res[0])
    print ('Key:', res[1])

# Now that the party is jumping    
