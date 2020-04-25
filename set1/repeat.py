import binascii

def to_hex(s):
    try:
        int(s, 16)
        return s
    except ValueError:
        return s.encode().hex()

def repeating_key_xor(s, key):
    res = "" 
    s = to_hex(s)
    key = to_hex(key)
    for i in range(0, len(s), len(key)):
        for j in range(i, min(len(s), i+len(key))):
            res += hex(int(s[j], 16)^int(key[j-i], 16))
    res = res.replace('0x', '')
    return res

if __name__ == '__main__': 
    inp = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    out = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    print(repeating_key_xor(inp, "ICE") == out)
