from reler.analysis.token import Token
from reler.analysis.token import TokenTypes

from reler.analysis.ast import AST
from reler.analysis.ast import CompoundNode
from reler.analysis.ast import AssignNode
from reler.analysis.ast import BinaryOperationNode
from reler.analysis.ast import UnaryOperationNode
from reler.analysis.ast import OdoNode
from reler.analysis.ast import EseNode
from reler.analysis.ast import ValueNode


class Parser:
    def __init__(self) -> None:
        self.stream = []
        self.index = 0

    def hasNextToken(self) -> bool:
        return len(self.stream) > self.index

    def currentToken(self) -> Token:
        return self.stream[self.index]

    def eat(self, tokenType: TokenTypes):
        token = self.currentToken()

        if token.type == tokenType:
            self.index += 1
            return
        
        raise SyntaxError(f"Unexpected Token { token.value }")

    def exprBool(self) -> AST:
        if self.currentToken().type == TokenTypes.DEIFIED:
            operator = self.currentToken()
            self.eat(TokenTypes.DEIFIED)

            identifier = self.currentToken()
            self.eat(TokenTypes.IDENTIFIER)
            
            return UnaryOperationNode(
                operator,
                identifier
            )

        identifier = self.currentToken()
        self.eat(TokenTypes.IDENTIFIER)

        operator = self.currentToken()
        self.eat(TokenTypes.GREATERTHAN)

        number = self.currentToken()
        self.eat(TokenTypes.NUMBER)

        return BinaryOperationNode(
            operator,
            identifier,
            number
        )

    def odo(self) -> OdoNode:
        self.eat(TokenTypes.ODO)

        condition = self.exprBool()
        statements = self.block()

        return OdoNode(
            condition,
            statements
        )

    def ese(self) -> EseNode:
        self.eat(TokenTypes.ESE)

        condition = self.exprBool()
        statements = self.block()

        return EseNode(
            condition,
            statements
        )

    def reler(self) -> UnaryOperationNode:
        operator = self.currentToken()
        self.eat(TokenTypes.RELER)

        literal = self.currentToken()
        self.eat(TokenTypes.LITERAL)

        return UnaryOperationNode(
            operator,
            literal
        )

    def assign(self) -> AssignNode:
        identifier = self.currentToken()
        self.eat(TokenTypes.IDENTIFIER)

        self.eat(TokenTypes.ASSIGN)

        if self.currentToken().type == TokenTypes.LITERAL:
            literal = self.currentToken()
            self.eat(TokenTypes.LITERAL)

            return AssignNode(
                identifier,
                ValueNode(literal)
            )

        if self.currentToken().type == TokenTypes.NUMBER:
            number = self.currentToken()
            self.eat(TokenTypes.NUMBER)
            
            return AssignNode(
                identifier,
                ValueNode(number)
            )

        if self.currentToken().type == TokenTypes.IDENTIFIER:
            lastIdentifier = self.currentToken()
            self.eat(TokenTypes.IDENTIFIER)
            
            operator = self.currentToken()
            self.eat(TokenTypes.MINUS)
            
            value = self.currentToken()
            self.eat(TokenTypes.NUMBER)

            return AssignNode(
                identifier,
                BinaryOperationNode(
                    operator,
                    lastIdentifier,
                    value
                )
            )

        raise SyntaxError("Assignment bad formed")

    def deified(self) -> UnaryOperationNode:
        operator = self.currentToken()
        self.eat(TokenTypes.DEIFIED)

        identifier = self.currentToken()
        self.eat(TokenTypes.IDENTIFIER)

        return UnaryOperationNode(
            operator,
            identifier
        )

    def statement(self) -> AST:
        if self.currentToken().type == TokenTypes.ODO:
            return self.odo()
        
        if self.currentToken().type == TokenTypes.ESE:
            return self.ese()

        if self.currentToken().type == TokenTypes.RELER:
            return self.reler()

        if self.currentToken().type == TokenTypes.IDENTIFIER:
            return self.assign()
        
        raise SyntaxError("Unrecognized statement")

    def statements(self):
        children = []
        
        while self.hasNextToken() and self.currentToken().type != TokenTypes.LER:
            child = self.statement()
            children.append(child)

        return CompoundNode(children)

    def block(self) -> CompoundNode:
        self.eat(TokenTypes.REL)
        node = self.statements()
        self.eat(TokenTypes.LER)

        return node

    def program(self) -> CompoundNode:
        return self.block()

    def parse(self, stream: list[Token]) -> CompoundNode:
        self.stream = stream
        self.index = 0

        return self.program()
    