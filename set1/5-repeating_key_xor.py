import binascii

def repeating_xor(s):
    key = "ICE"
    res = ""
    for i in range(0, len(s), 3):
        res += chr(ord(s[i])^ord(key[0]))
        if(i+1 < len(s)):
            res += chr(ord(s[i+1])^ord(key[1]))
        if(i+2 < len(s)):
            res += chr(ord(s[i+2])^ord(key[2]))
    res = binascii.hexlify(res.encode())
    res = str(res, 'ascii')
    return res

inp = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
out = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

print(repeating_xor(inp) == out)
