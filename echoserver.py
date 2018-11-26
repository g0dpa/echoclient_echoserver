import socketserver
import threading
import sys

class UserManager:

    def __init__(self):
        self.users = {}

    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send('Already used ID\n')
            return None

        lock.acquire()
        self.users[username] = (conn, addr)
        lock.release()

        self.sendMessageToAll('User [%s] participates.' % username)
        return username

    def removeUser(self, username):
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('User [%s] quits...' % username)

    def messageHandler(self, username, msg, option):

        if msg.strip() == '/quit':
            self.removeUser(username)
            return -1

        if(option == 'Y'):
            self.sendMessageToAll('[%s] %s' % (username, msg))
            return
        elif(option == 'N'):
            self.sendMessageToUser(username, '[%s] %s' % (username, msg))

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg)

    def sendMessageToUser(self,username, msg):
        conn, addr = self.users[username]
        conn.send(msg)

class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):
        print('[%s] Connected' % self.client_address[0])

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg)
                if(OPTION == 'Y'):
                    if self.userman.messageHandler(username, msg, 'Y') == -1:
                        self.request.close()
                        break
                elif(OPTION == 'N'):
                    if self.userman.messageHandler(username, msg, 'N') == -1:
                        self.request.close()
                        break
                msg = self.request.recv(1024)
        except Exception as e:
            print(e)

        print('[%s] Quit' % self.client_address[0])
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send('Your name: ')
            username = self.request.recv(1024)
            if self.userman.addUser(username, self.request, self.client_address):

                return username

class SetServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer():
    print('+++ Server Running')
    print('+++ If you want to Quit, Press Ctrl-C')

    try:
        server = SetServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('--- Server OUT....')
        server.shutdown()
        server.server_close()


if __name__=='__main__':

    try:
        HOST='localhost'
        PORT=int(sys.argv[1])
        if(len(sys.argv) == 3 and sys.argv[2] == '-b'):
            OPTION = 'Y'
        elif(len(sys.argv) == 2):
            OPTION = 'N'
        else:
            sys.exit(1)
        lock = threading.Lock()
        runServer()
    except:
        print("syntax : python echoserver.py <port> [-b]")
