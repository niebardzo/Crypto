# Implementation of Ceaser Cipher.
#
# No requirements to run.
#
# Author: Patryk Bogusz
#




def encode(key, messaage):
	"""
	The function inteded to encode a message with a given key.
	"""
	encoded = ''
	for word in message:
		for letter in word:
			letter = ord(letter) + key
			if letter > 90:
				letter = letter - 26
			encoded = encoded + chr(letter)
		encoded= encoded + ' '
	return encoded



while True:	
	try:
		key = int(input("What is the key? "))
		if key >= 26 or key <= 0:
			raise ValueError
	except ValueError:
		print("The key must be integer")
		continue
	else:
		break
while True:
	try:
		message = str(input("What is the message? [A-Z] ")).upper().split()
		for msg in message:
			if not msg.isalpha():
				raise ValueError
	except ValueError:
		print("The message should only contain characters from A to Z.")
		continue
	else:
		print(encode(key, message))
		break
