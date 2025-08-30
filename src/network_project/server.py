import socket
from src.common.config import ConnectionConfig
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 65432)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

class ChatServer:
    def __init__(self):
        self.connections = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ConnectionConfig
        print(f'starting up on {server_address}')
        self.sock.bind((ConnectionConfig.host, ConnectionConfig.port))
        self.sock.listen(5)

    def run(self):
        while True:
           print('waiting for a connection')
           connection, client_address = sock.accept()
           try:
               print('connection from', client_address)
               while True:
                   data = connection.recv(1024)
                   print('received {!r}'.format(data))
                   if data:
                       print('sending data back to the client')
                       connection.sendall(data.upper())
                   else:
                       print('no data from', client_address)
                       break
           finally:
               connection.close()
