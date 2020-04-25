def fixed_xor(s, t):
    hs = int(s, 16)
    ht = int(t, 16)
    hs = hs^ht
    out = (hex(hs).lstrip('0x'))
    return out

if __name__ == '__main__':
    s = "1c0111001f010100061a024b53535009181c"
    t = "686974207468652062756c6c277320657965"
    res = "746865206b696420646f6e277420706c6179"
    print (fixed_xor(s, t) == res)
