from enum import Enum
from enum import auto

class UnrecognizedTokenError(Exception):
    pass

class MalformedTokenError(Exception):
    pass

class IdentifierNameError(Exception):
    pass

class TokenTypes(Enum):
    REL = auto()
    LER = auto()
    ODO = auto()
    ESE = auto()
    RELER = auto()
    LITERAL = auto()
    NUMBER = auto()
    GREATERTHAN = auto()
    WHITESPACE = auto()
    IDENTIFIER = auto()
    DEIFIED = auto()
    ASSIGN = auto()
    MINUS = auto()

class Token:
    def __init__(self, value, _type: TokenTypes) -> None:
        self.value = value
        self.type = _type

    def __repr__(self) -> str:
        return f"Token({ self.value }, { self.type.name })"
