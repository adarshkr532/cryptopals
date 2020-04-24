def base64_to_hex(inp):
    base64key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    hexkey = "0123456789abcdef"
    out = ""
    for i in range(0, len(inp), 2):
        if(inp[i] == '='):
            val1 = 0
        else:
            val1 = base64key.index(inp[i])
        if(inp[i+1] == '='):
            val2 = 0
        else:
            val2 = base64key.index(inp[i+1])
        c = val1*64 + val2
        out += hexkey[c//256]
        c = c - (c//256)*256
        out += hexkey[c//16]
        out += hexkey[c%16]
    return out

if __name__ == "__main__":
    inp = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    req = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    print (base64_to_hex(inp) == req)
