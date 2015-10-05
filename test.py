from configparser import ConfigParser
from rsa import RSA
import tools
import sys

lorem = "Lorem ipsm dolor sit amet, ibh at nisl tincidunt, et faucibus risus suscipit. Nunc cursus facilisis felis. Sed a urna eget felis dignissim tincidunt. Mauris eget dapibus lorem, sed mattis quam. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam pellentesque accumsan gravida. Sed quis nisi est. Curabitur lorem purus, pellentesque dictum urna et, ultrices vulputate ex. Sed condimentum posuere felis, et gravida leo feugiat vel.In tempus a mauris vitae luctus. Suspendisse fermentum nibh mauris, ut elementum magna pretium non. Cras imperdiet orci magna, quis pretium ipsum ullamcorper eget. Vivamus sagittis vehicula eros. Cras rutrum ante eleifend orci aliquet, a mattis diam semper. Morbi nec pharetra est. Ut pretium ante pharetra nunc hendrerit porta. Suspendisse lacinia orci at semper tristique. Vivamus in orci leo. Mauris enim dui, faucibus nec porttitor quis, interdum sed eros. Nunc non rhoncus lacus, nec laoreet felis.Nulla ut velit id libero scelerisque tincidunt sed ullamcorper est. Aliquam quam odio, ullamcorper in posuere a, dapibus sit amet elit. Maecenas mollis commodo quam, eget molestie mauris aliquam id. Morbi consectetur dignissim quam, eget sodales diam semper id. Nulla vestibulum non turpis a commodo. Nunc quis nisl lectus. Suspendisse dignissim Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse blandit nibh at nisl tincidunt, et faucibus risus suscipit. Nunc cursus facilisis felis. Sed a urna eget felis dignissim tincidunt. Mauris eget dapibus lorem, sed mattis quam. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam pellentesque accumsan gravida. Sed quis nisi est. Curabitur lorem purus, pellentesque dictum urna et, ultrices vulputate ex. Sed condimentum posuere felis, et gravida leo feugiat vel.In tempus a mauris vitae luctus. Suspendisse fermentum nibh mauris, ut elementum magna pretium non. Cras imperdiet orci magna, quis pretium ipsum ullamcorper eget. Vivamus sagittis vehicula eros. Cras rutrum ante eleifend orci aliquet, a mattis diam semper. Morbi nec pharetra est. Ut pretium ante pharetra nunc hendrerit porta. Suspendisse lacinia orci at semper tristique. Vivamus in orci leo. Mauris enim dui, faucibus nec porttitor quis, interdum sed eros. Nunc non rhoncus lacus, nec laoreet felis.Nulla ut velit id libero scelerisque tincidunt sed ullamcorper est. Aliquam quam odio, ullamcorper in posuere a, dapibus sit amet elit. Maecenas mollis commodo quam, eget molestie mauris aliquam id. Morbi consectetur dignissim quam, eget sodales diam semper id. Nulla vestibulum non "

if __name__ == "__main__":

	pub_f = ConfigParser()
	pub_f.read("customers/toto/public.key")
	pub_rsa = RSA(int(pub_f["key"]["n"]), e=int(pub_f["key"]["e"]))

	pri_f = ConfigParser()
	pri_f.read("customers/toto/private.key")
	pri_rsa = RSA(int(pri_f["key"]["n"]), d=int(pri_f["key"]["d"]))

	sign = pri_rsa.sign(lorem)




	# lorem = str(len(lorem)) + lorem

	# lorem_int = tools.text_to_int(lorem)
	# sign = pri_rsa.sign(lorem_int)
	decode = pub_rsa.check_signature(sign)

	print("Len lorem " + str(len(lorem)))
	print("Len decode " + str(len(decode)))
	if decode == lorem:
		print("YARP")


	# check = pub_rsa.check_signature(sign)
	# decode_lorem = ""
	# for c in check:
	# 	v = int_to_string(c)
	# 	decode_lorem += v

	# f1 = open("orig", 'w')
	# f1.write(str(lorem_int))
	# f1.close()

	# f1 = open("dec", 'w')
	# for c in check:
	# 	print(len(str(c)), end=" ")
	# 	size += len(str(c))
	# 	if len(str(c)) == 99:
	# 		print("Adding left padding")
	# 		f1.write("0")
	# 	else:
	# 		print()
	# 	f1.write(str(c))
	# f1.close()

	# print(len(lorem))
	# print(size)

	# print(string_to_int("ToTo123"))
	# print(int_to_string(string_to_int("ToTo123")))
