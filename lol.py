def text_to_int(text):
	"""Convert the ascii text given as string to an integer"""
	integer = 0
	for c in text:
		integer = integer << 8
		integer = integer + ord(c)
	return integer


def int_to_text(integer):
	"""Convert the given number as an asciistring """
	text = ""
	while integer>0:
		char = chr(integer & 0xFF)
		text = char + text
		integer = integer >> 8
	return text[:-1]
