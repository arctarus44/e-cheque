import binascii

def text_to_int(text):
	"""Convert the ascii text given as string to an integer"""
	hex_repr = binascii.hexlify(text.encode("ascii"))
	return int(hex_repr.decode("ascii"), 16)

def int_to_text(integer):
	"""Convert the given number as an asciistring """
	hex_repr = hex(integer)[2:]	# skipping the 0x
	if len(hex_repr) % 2 != 0:
		hex_repr = "0" + hex_repr
	return binascii.unhexlify(hex_repr).decode("ascii")
