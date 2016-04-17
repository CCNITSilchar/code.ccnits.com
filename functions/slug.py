ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def encode(num, alphabet=ALPHABET):
	string_stack = []
	base = len(alphabet)
	while num:
		rem = num % base
		num = num // base
		string_stack.append(alphabet[rem])
	string_stack.reverse()
	string = ''.join(string_stack)
	strlen = len(string)
	if strlen < 4:
		string = 'a' * (4 - strlen) + string
	return string


def decode(string, alphabet=ALPHABET):
	base = len(alphabet)
	strlen = len(string)
	num = 0
	idx = 0
	for char in string:
		power = (strlen - (idx + 1))
		num += alphabet.index(char) * (base ** power)
		idx += 1

	return num
