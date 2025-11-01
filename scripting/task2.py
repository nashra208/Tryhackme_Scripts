
import socket

# Hard-coded IP
target_ip = <IP_address>

# Declaring request snippet
request = "GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % target_ip

port = 1337  # Starting port
value = 0    # Starting value
waiting = False
print('Port:', port)

while True:
    try:
        # establishing the connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, int(port)))
        # sending the request declared above
        s.send(request.encode())
        r = s.recv(1024)
        r = r.decode().split('\n')[-1] # spliiting and grabbing the last part which is port number example : minus 2 8888
        if r != '': # here is the response is not empty 
            print('->', r) # print the response

        if "STOP" in r:
            break  # if response has STOP then  break out of the loop

        operation, v, port = r.split(' ')  #split the string --example: minus 2 8888 -- ['minus', '2' , '8888']
        if operation == 'add':
            value += float(v)
        if operation == 'minus':
            value -= float(v)
        if operation == 'multiply':
            value *= float(v)
        if operation == 'divide':
            value /= float(v)

        print('-' * 32)
        print('Port:', port)
        waiting = False

    except ConnectionRefusedError:
        if not waiting:
            print('Waiting for connection...')
            waiting = True
    except ValueError:
        pass
# When ConnectionRefusedError happens → it never reaches the part that splits or updates the value, because the connection didn’t succeed.

# The waiting = True just sets the flag so the message prints only once.

# The script then loops back (while True) and tries to connect again.

# Only after a successful connection does it read the response, split it, and apply the operation to value.
print("\nValue: %.2f" % value)
            
           

