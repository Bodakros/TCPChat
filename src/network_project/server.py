import socket
import json
from src.common.config import ConnectionConfig

class CaesarCipher:
    @staticmethod
    def encrypt(text: str, shift: int) -> str:
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result

class ChatServer:
    def __init__(self):
        self.connections = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (ConnectionConfig.host, ConnectionConfig.port)
        print(f'starting up on {self.server_address[0]} port {self.server_address[1]}')
        self.sock.bind(self.server_address)
        self.sock.listen(5)
        self.cipher = CaesarCipher()

    def handle_client_message(self, connection):
        try:
            # Получаем ключ шифрования
            key_data = connection.recv(1024)
            if not key_data:
                print("Client closed connection while sending key")
                return False

            try:
                message_data = json.loads(key_data.decode())
                if 'shift' not in message_data:
                    print("Error: 'shift' field not found in message")
                    connection.sendall("Error: Invalid key format".encode())
                    return True

                key = message_data['shift']
                if not isinstance(key, int) or not (1 <= key <= 25):
                    print("Error: shift must be an integer between 1 and 25")
                    connection.sendall("Error: Shift must be between 1 and 25".encode())
                    return True

            except json.JSONDecodeError:
                print("Error: Invalid JSON format received")
                connection.sendall("Error: Invalid JSON format".encode())
                return True

            # Получаем сообщение для шифрования
            data = connection.recv(1024)
            if not data:
                print("Client closed connection while sending message")
                return False

            message = data.decode()
            print(f'Received message: {message}')

            # Шифруем сообщение
            encrypted_message = self.cipher.encrypt(message, key)
            print(f'Encrypted message (shift={key}): {encrypted_message}')

            # Отправляем зашифрованное сообщение обратно
            connection.sendall(encrypted_message.encode())
            return True

        except Exception as e:
            print(f"Error processing message: {e}")
            try:
                connection.sendall(f"Server error: {str(e)}".encode())
            except:
                pass
            return False

    def run(self):
        while True:
            print('waiting for a connection')
            connection, client_address = self.sock.accept()
            try:
                print('connection from', client_address)
                while self.handle_client_message(connection):
                    pass
            finally:
                connection.close()
