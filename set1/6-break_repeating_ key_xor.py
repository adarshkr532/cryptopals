import binascii

def hamming_distance(s, t):
    dis = 0
    for i in range(0, len(s)):
        p = ord(s[i])^ord(t[i])
        dis += bin(p).count('1')
    return dis

s = "this is a test"
t = "wokka wokka!!!"
print (hamming_distance(s, t))
