import socket
import sys
from threading import Thread

def rcvMsg(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data)
        except:
            pass

def runClient():

    try:
        t = Thread(target = rcvMsg, args = (sock,))
        t.daemon = True
        t.start()

        while True:
            msg = raw_input()
            sock.send(msg)
            if(msg == '/quit'):
                break
    except:
        pass

if __name__=='__main__':

    try:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
        if(len(sys.argv) != 3):
            sys.exit(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST,PORT))
    except:
        print("syntax: python echoclient.py <host> <port>")

    try:
        runClient()
    except:
        sock.close()
        sys.exit()
