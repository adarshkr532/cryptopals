# The biggest disadvantage of ECB mode is lack of diffusion. Same 16-byte plaintext
# will always produce same ciphertext for a particular key

def score(data):
	block = [data[i:i+16] for i in range(0, len(data), 16)]
	return len(block) - len(set(block))

if __name__ == '__main__':
	
	with open('8.txt', 'r') as file:
		data = file.readlines()

	max_score = 0
	cipher = ""
	for i in data:
		cur_score = score(i)
		if(cur_score > max_score):
			max_score = cur_score
			cipher = i
	block = [cipher[i:i+16] for i in range(0, len(cipher), 16)]
	print(block)