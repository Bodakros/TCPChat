import socket
from src.common.config import ConnectionConfig

class UDPChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (ConnectionConfig.host, ConnectionConfig.port)

    def send_message(self, message):
        try:
            print(f'Sending {message!r} to {self.server_address}')
            self.sock.sendto(message.encode(), self.server_address)

            data, server = self.sock.recvfrom(1024)
            print(f'Received {data!r} from {server}')
            return data.decode()

        except Exception as e:
            print(f'Error: {e}')
            return None

    def close(self):
        self.sock.close()

if __name__ == '__main__':
    client = UDPChatClient()
    while True:
        message = input("Enter message (or 'quit' to exit): ")
        if message.lower() == 'quit':
            break
        response = client.send_message(message)
    client.close()
