from dataclasses import dataclass

@dataclass
class ConnectionConfig:
    host: str = '127.0.0.1'
    port: int = 25565
