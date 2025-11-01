from cryptography.hazmat.primitives.ciphers.modes import GCM
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag
import socket 
import hashlib

server_ip = "10.10.165.40"
port = 4000

# first creating socket object 
# DGRAM is used for udp connection 

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# optional: set a timeout so recvfrom won't block forever while you're testing
# client.settimeout(5.0)

request1 = client.sendto('hello'.encode(), (server_ip, port))
response1 = client.recvfrom(4069)
print(f"Response from tryhackme udp server: {response1}")

print("\n")

request2 = client.sendto('ready'.encode(), (server_ip, port))
response2 = client.recvfrom(4069)
print(f"Second response from tryhackme udp server: {response2}")
print("\n")

# words_in_response2[0] → b'key:thisisaverysecretkeyl337'
# .split(b':') → [b'key', b'thisisaverysecretkeyl337']
# [1] picks the second part → the key value

words_in_response2 = response2[0].split()
KEY = words_in_response2[0].split(b':')[1]
IV = words_in_response2[1].split(b':')[1]

checksum_to_find = response2[0].split()[14]

# response2[0].split()[14]
# Just picks the 15th word (index 14) in the split list, which is the checksum bytes.

print("\n---\nKey: {}\nIV: {}\nChecksum to find: {}\n---\n".format(KEY.decode(), IV.decode(), checksum_to_find.hex())) # .format() is used to insert values into {} placeholders in a string.
                                                                                                                       #.hex() → converts binary bytes to a readable hex string
                                                                                                                       #.decode() -> converting the bytes to text
                                                                                                            
# function for decryption of flag
def decryption(ciphertext, key, iv, tag):
    # IMPORTANT: call finalize() after update() to verify the GCM tag.
    decryptor = Cipher(AES(key), GCM(iv, tag), backend=default_backend()).decryptor()
    plaintext = decryptor.update(ciphertext)
    # finalize() will raise InvalidTag if authentication fails
    decryptor.finalize()
    return plaintext


while True:
    client.sendto('final'.encode(), (server_ip, port))
    encrypted_text = client.recvfrom(4069)
    print(f'Encrypted text: {encrypted_text[0].hex()}\n')
    
    client.sendto("final".encode(), (server_ip, port))
    tag = client.recvfrom(1024)
    print(f'TAG : {tag[0].hex()}')
    
    try:
        decrypted_text = decryption(encrypted_text[0], KEY, IV, tag[0])
    except InvalidTag:
        print("InvalidTag: authentication failed for this ciphertext/tag — trying next packet.\n")
        # continue loop to request next ciphertext (server likely expects repeated "final" calls)
        continue

    # show the decrypted bytes (and attempt to decode nicely)
    try:
        printable = decrypted_text.decode()
    except UnicodeDecodeError:
        printable = decrypted_text.decode(errors='replace')
    print("Decrypted (decoded if possible):", printable)
    
    current_hash = hashlib.sha256(decrypted_text).hexdigest()
    print("Current hash: ", current_hash)
    
    if(current_hash == checksum_to_find.hex()):
        print("\n===\nWoohoo!! u cracked it '{}'\n===\n".format(printable))
        
        break
