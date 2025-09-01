import socket
import json
from src.common.config import ConnectionConfig

class ChatClient:
    def __init__(self):
        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (ConnectionConfig.host, ConnectionConfig.port)
        print(f'connecting to {self.server_address}')
        try:
            self.sock.connect(self.server_address)
        except Exception as e:
            print(f'Connection failed: {e}')
            self.sock = None

    def send_message(self, message: str, shift: int):
        if not self.sock:
            print("Not connected. Attempting to reconnect...")
            self.connect()
            if not self.sock:
                return None

        try:
            key_data = json.dumps({'shift': shift}).encode()
            self.sock.sendall(key_data)
            self.sock.sendall(message.encode())
            encrypted_response = self.sock.recv(1024).decode()
            if not encrypted_response:
                print("Connection lost. Server closed the connection.")
                self.sock.close()
                self.sock = None
                return None

            print(f'Received encrypted response: {encrypted_response}')
            return encrypted_response

        except Exception as e:
            print(f'Error occurred: {e}')
            self.sock.close()
            self.sock = None
            return None

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

def main():
    client = ChatClient()
    try:
        while True:
            message = input("Enter message (or 'quit' to exit): ")
            if message.lower() == 'quit':
                break

            try:
                shift = int(input("Enter shift key (1-25): "))
                if not 1 <= shift <= 25:
                    print("Shift key must be between 1 and 25")
                    continue
            except ValueError:
                print("Please enter a valid number")
                continue

            response = client.send_message(message, shift)
            if not response:
                print("Failed to send message. Will try to reconnect on next message.")

    finally:
        client.close()

if __name__ == "__main__":
    main()
