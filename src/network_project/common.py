from dataclasses import dataclass

class Error:
    instance_count = 0
    def __init__(self, message):
        self.message = message
        Error.instance_count += 1
        self.code = Error.instance_count

@dataclass
class Errors:
    nickname_error = Error('This nicname is already taken. Please choose another one.')
    nickname_empty = Error('Nickname cannot be empty.')



