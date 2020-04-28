import binascii

def pkcs7_padding(text, padding):
	b = bytearray()
	b.extend(map(ord, text))
	for i in range(padding):
		b.append(padding)
	return b

if __name__ == '__main__':
	
	text = "YELLOW SUBMARINE"
	
	print(pkcs7_padding(text, 4))