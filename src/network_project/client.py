import argparse
import socket
from src.common.config import ConnectionConfig

class Client:
    def __init__(self):
        self.port = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def run(self):
        self.sock.connect((ConnectionConfig.host, ConnectionConfig.port))





