import socket 

# setting up the target 
host = <IP_Address>

port = 8000

# setting the wordlist for fuzzing 
wordlist_file = "/home/nashra/SecLists-master/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt"

# function for fuzzing the endpoint 
def fuzz_endpoint(wordlist_file):
    try:
         with open(wordlist_file, 'r') as file:
             for line in file:
                command = line.strip()
            # establishing the connection to the server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host,port))
                    # send the words to the target
                    # b'\n' is just a bytes version of the newline.
                    s.sendall(command.encode() + b'\n')
                    # The code reads up to 1024 bytes from the socket, decodes to text, and strips whitespace.
                    response = s.recv(1024).decode().strip()
                    # logic to cath valid response 
                    if response != "" and "is not defined" not in response and "leading zeros in decimal integer literals are not permitted" not in response and "invalid syntax" not in response :
                        print(f"🥶 U cracked the payload {command}")
                        print(f"🥶 Response: {response}")
    except FileNotFoundError:
        print(f"Yoo u using file that aint existing!")
    except Exception as e:
        print(f"an error occured {e}")
        
        
# run the function 
fuzz_endpoint(wordlist_file)
                
                
                
            




# AF_INET → IPv4

# SOCK_STREAM → TCP
# a stream means a continuous flow of bytes
# TCP is a transport-layer protocol (not the lowest network level).
#     • A socket is the OS/API object you use to talk over TCP (or UDP).
#     • socket.send / sendall accept raw bytes, yes — the socket API sends bytes and the OS breaks them into TCP segments and hands them to lower layers.
#     • For text you must encode (str → bytes) before sending and decode bytes → str after recv.
#     • Bonus: TCP is a stream, so data may arrive split or merged — your code must handle partial reads.
# != only checks for exact match, not if a phrase appears inside a longer string.

# For partial phrases, you need not in.
