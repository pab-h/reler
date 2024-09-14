from reler.token import IdentifierNameError, Token
from reler.token import TokenTypes
from reler.token import MalformedTokenError
from reler.token import UnrecognizedTokenError

class Lexer:
    def __init__(self) -> None:
        self.buffer = ""
        self.index = 0

        self.keywords = {
            "Rel": Token(
                "Rel",
                TokenTypes.REL
            ),
            "leR": Token(
                "leR",
                TokenTypes.LER
            ),
            "odo": Token(
                "odo",
                TokenTypes.ODO
            ),
            "ese": Token(
                "ese",
                TokenTypes.ESE
            ),
            "reler": Token(
                "reler",
                TokenTypes.RELER
            ),
            "deified": Token(
                "deified",
                TokenTypes.DEIFIED
            )
        }
        
    def hasNextToken(self) -> bool:
        return len(self.buffer) > self.index
    
    def currentChar(self) -> str:
        return self.buffer[self.index]

    def isPalindrome(self, name) -> bool:
        return name == name[::-1]

    def identifier(self) -> Token:
        identifier = ""

        while self.hasNextToken() and self.currentChar().isalpha():
            identifier += self.currentChar()
            self.index += 1

        token = self.keywords.get(
            identifier,
            Token(
                identifier,
                TokenTypes.IDENTIFIER
            )
        )

        if token.type == TokenTypes.IDENTIFIER:
            if not self.isPalindrome(token.value):
                raise IdentifierNameError(f"identifier { token.value } is not a Palindrome!")

        return token

    def assign(self) -> Token:
        assign = self.currentChar()
        self.index += 1

        if self.hasNextToken() and self.currentChar() == "=":
            assign += self.currentChar()
            self.index += 1

        if self.hasNextToken() and self.currentChar() == ":":
            assign += self.currentChar()
            self.index += 1

        if assign != ":=:":
            raise MalformedTokenError(f"Malformed attribution token: { assign }")
        
        return Token(
            assign,
            TokenTypes.ASSIGN
        )

    def number(self) -> Token:
        number = self.currentChar()
        self.index += 1

        while self.hasNextToken() and self.currentChar().isnumeric():
            number += self.currentChar()
            self.index += 1

        return Token(
            int(number),
            TokenTypes.NUMBER
        )

    def literal(self) -> Token:
        literal = "" 
        self.index += 1

        while self.hasNextToken() and self.currentChar() != "\"":
            literal += self.currentChar()
            self.index += 1

        self.index += 1
        return Token(
            literal,
            TokenTypes.LITERAL
        )

    def nextToken(self) -> Token:
        if not self.hasNextToken():
            return None

        currentChar = self.currentChar()

        if currentChar == "-":
            token = Token(
                "-",
                TokenTypes.MINUS
            )

            self.index += 1

            return token

        if currentChar == "\"":
            return self.literal()

        if currentChar.isnumeric():
            return self.number()

        if currentChar == ">":
            token = Token(
                ">",
                TokenTypes.GREATERTHAN
            )

            self.index += 1

            return token
        
        if currentChar.isspace():
            token = Token(
                " ",
                TokenTypes.WHITESPACE
            )

            self.index += 1

            return token

        if currentChar == ":":
            return self.assign()

        if currentChar.isalpha():
            return self.identifier()
        
        raise UnrecognizedTokenError(f"Unrecognized token: { currentChar }")

    def lex(self, buffer) -> list[Token]:
        self.buffer = buffer
        self.index = 0

        tokens = []

        while self.hasNextToken():
            token = self.nextToken()

            if token.type == TokenTypes.WHITESPACE:
                continue

            tokens.append(token)

        return tokens