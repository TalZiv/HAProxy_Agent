'''
    Simple socket server using threads
'''
import signal
import socket
import psutil
from _thread import *
import sys
import json

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        s.close()
        print('Closed Socket')
        sys.exit(0)

#print('Press Ctrl+C')
#signal.pause()

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
signal.signal(signal.SIGINT, signal_handler)

print('Socket created')

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

# Start listening on socket
s.listen(10)
print('Socket now listening')


# Function for handling connections. This will be used to create threads
def clientthread(conn):
    # Sending message to connected client
    #conn.send(b'Welcome to the server. Type something and hit enter\n')  # send only takes string

    with open('agent_config.json', mode='r') as data_file:
        data = json.load(data_file)
    if data['state'] == 'Normal':
        print('state Normal')
        if data['LastStatus'] == 1 :
            idle = bytes(str(int(100 - psutil.cpu_percent(interval=0.5))), encoding='utf8')
            conn.send(b'up ready ' + idle + b'%\r\n')  # literla percent sign
            conn.close()
            with open('agent_config.json', mode='w') as data_file:
                data['LastStatus'] = 0
                data_file.write(json.dumps(data))
        else:
            idle = bytes(str(int(100 - psutil.cpu_percent(interval=0.5))), encoding='utf8')
            conn.send(idle + b'%\r\n')  # literla percent sign
            conn.close()
    elif data['state'] == 'Down' :
        conn.send(b'down\r\n')
    elif data['state'] == 'drain' :
        conn.send(b'down\r\n')
    else:
        conn.send(b'bla\r\n')
    # infinite loop so that function do not terminate and thread do not end.
    #while True:

        # Receiving from client
        #data = conn.recv(1024)
        #reply = b'OK...' + data
        #if not data:
        #    break

        #conn.sendall(reply)
    #    conn.sendall(b'Go Away')

    # came out of loop



# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))

s.close()
