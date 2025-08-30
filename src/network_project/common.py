from dataclasses import dataclass
from enum import Enum

@dataclass
class Event:
    code: int
    message: str

class Error(Event):
    instance_count = 0
    def __init__(self, message: str):
        Error.instance_count += 1
        super().__init__(Error.instance_count, message)

class Errors(Event):
    nickname_error = Error('This nicname is already taken. Please choose another one.')
    nickname_empty = Error('Nickname cannot be empty.')


class Options(Event, Enum):
    instance_count = 0
    def __init__(self, message: str):
        super().__init__(Error.instance_count, message)

