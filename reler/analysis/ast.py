from enum import Enum
from enum import auto

from reler.analysis.token import Token

class ASTType(Enum):
    ABSTRACT = auto()
    UNARY = auto()
    BINARY = auto()
    ASSIGN = auto()
    COMPOUND = auto()
    ODO = auto()
    ESE = auto()
    VALUE = auto()
    IDENTIFIER = auto()

class AST:
    def __init__(self) -> None:
        self.type = ASTType.ABSTRACT

class UnaryOperationNode(AST): 
    def __init__(self, operator: Token, value: AST) -> None:
        super().__init__()

        self.type = ASTType.UNARY
        self.operator = operator
        self.value = value

class BinaryOperationNode(AST):
    def __init__(self, operator: Token, left: AST, right: AST) -> None:
        super().__init__()

        self.type = ASTType.BINARY
        self.operator = operator
        self.left = left
        self.right = right

class AssignNode(AST):
    def __init__(self, identifier: Token, value: AST) -> None:
        super().__init__()

        self.type = ASTType.ASSIGN
        self.identifier = identifier
        self.value = value

class CompoundNode(AST):
    def __init__(self, children: list[AST]) -> None:
        super().__init__()

        self.type = ASTType.COMPOUND
        self.children = children

class OdoNode(AST):
    def __init__(self, condition: AST, statements: CompoundNode) -> None:
        super().__init__()

        self.type = ASTType.ODO

        self.condition = condition
        self.statements = statements

class EseNode(AST):
    def __init__(self, condition: AST, statements: CompoundNode) -> None:
        super().__init__()

        self.type = ASTType.ESE

        self.condition = condition
        self.statements = statements

class ValueNode(AST):
    def __init__(self, value: Token) -> None:
        super().__init__()

        self.type = ASTType.VALUE

        self.value = value 

class IdentifierNode(AST):
    def __init__(self, identifier: Token) -> None:
        super().__init__()

        self.type = ASTType.IDENTIFIER

        self.identifier = identifier
