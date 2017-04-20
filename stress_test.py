import socket
import sys
from _thread import *
from time import sleep


def connectSocket():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.setblocking(True)
    sock.settimeout(5)
    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 8888)
    #print ('connecting to %s port %s\r\n' % server_address)
    sock.connect(server_address)

    try:
        #sleep(1)
        #data=''
        #while len(data) <= 3:
        data = sock.recv(16)
        print('received ' + str(data, encoding='utf8'))
    except:
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        #print('closing socket')
        sock.close()


for _ in range(5):
    start_new_thread(connectSocket,())
    sleep(0.5)
