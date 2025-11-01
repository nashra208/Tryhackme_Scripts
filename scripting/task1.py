
        

import base64

# base64 in decoding first gives bytes and then convert that into readable form 

def decoding_the_flag(a):
    decode_flag = a.strip()  # remove any newline characters
    for i in range(50):
        decode_flag = base64.b64decode(decode_flag) # This will return bytes
    print(decode_flag.decode())  # decode from bytes to string

filename = 'b64_1550406728131.txt'
with open(filename, 'r') as file:
    for line in file:
        decoding_the_flag(line)

    