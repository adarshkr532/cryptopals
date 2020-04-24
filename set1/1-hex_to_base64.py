inp = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
base64key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
hexkey = "0123456789abcdef"
out = ""
req = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
for i in range(0, len(inp), 3):
    val1 = int(inp[i], 16)
    val2 = int(inp[i+1], 16)
    val3 = int(inp[i+2], 16)
    c = val1*4 + val2//4
    out += base64key[c]
    c = (val2%4)*16 + val3
    out += base64key[c]
print (req)
print (out)
print (out == req)
