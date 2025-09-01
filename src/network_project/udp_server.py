import socket
from src.common.config import ConnectionConfig

class UDPChatServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f'Starting UDP server on {ConnectionConfig.host}:{ConnectionConfig.port}')
        self.sock.bind((ConnectionConfig.host, ConnectionConfig.port))

    def run(self):
        print('UDP Server is listening...')
        while True:
            try:
                data, client_address = self.sock.recvfrom(1024)
                print(f'Received {data!r} from {client_address}')
                
                if data:
                    response = data.upper()
                    print(f'Sending response back to {client_address}')
                    self.sock.sendto(response, client_address)
            except Exception as e:
                print(f'Error: {e}')

if __name__ == '__main__':
    server = UDPChatServer()
    server.run()
