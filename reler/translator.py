from reler.analysis.ast import *

from reler.analysis.token import TokenTypes

class Translator:
    def __init__(self) -> None:
        self.deep = 0
        
        self.deifiedFunc = """def deified(value: str) -> bool:\n\tvalue = value.replace(" ", "").lower()\n\treturn value == value[::-1]\n\n"""
        self.reler = """def reler(value: str):\n\tif deified(value):\n\t\treturn value\n\tprint(value + " | " + value[::-1])\n\n"""

    def visitCompound(self, node: CompoundNode) -> str:
        statements = ""

        ident = "\t" * self.deep

        self.deep += 1
        for child in node.children:
            statements += ident + self.visit(child) + "\n"

        self.deep += -1

        return statements

    def visitAssign(self, node: AssignNode) -> str:
        identifier = node.identifier.value
        value = node.value

        return f"{identifier} = {self.visit(value)}"

    def formatLiteral(self, literal: str) -> str:
        literalFormated = list(literal)
        
        i = 0
        openKey = True

        for char in literal:
            if char != "%":
                literalFormated[i] = literal[i]
                i += 1  

                continue          

            if openKey:
                literalFormated[i] = "{"
            else:
                literalFormated[i] = "}"

            openKey = not openKey
            i += 1  
        
        return "f\"" + "".join(literalFormated) + "\""
    
    def visitValue(self, node: ValueNode) -> str:
        token = node.value

        if token.type == TokenTypes.LITERAL:
            return self.formatLiteral(token.value)
        
        return str(token.value)

    def visitBinary(self, node: BinaryOperationNode) -> str:
        return self.visit(node.left) + \
                f" {node.operator.value} " + \
                self.visit(node.right)

    def visitUnary(self, node: UnaryOperationNode) -> str:
        value = self.visit(node.value)

        if node.operator.type == TokenTypes.DEIFIED:
            self.hasDeified = True

            return f"deified({value})"
        
        return f"reler({value})"

    def visitIdentifier(self, node: IdentifierNode) -> str:
        return node.identifier.value

    def visitEse(self, node: EseNode) -> str:
        condition = self.visit(node.condition)
        statements = self.visit(node.statements)

        return f"if {condition}:\n{statements}"

    def visitOdo(self, node: OdoNode) -> str:
        condition = self.visit(node.condition)
        statements = self.visit(node.statements)

        return f"while {condition}:\n{statements}"

    def visit(self, node: AST) -> str:
        if node.type == ASTType.COMPOUND:
            return self.visitCompound(node)

        if node.type == ASTType.ASSIGN:
            return self.visitAssign(node)

        if node.type == ASTType.VALUE:
            return self.visitValue(node)

        if node.type == ASTType.BINARY:
            return self.visitBinary(node)

        if node.type == ASTType.UNARY:
            return self.visitUnary(node)

        if node.type == ASTType.IDENTIFIER:
            return self.visitIdentifier(node)
        
        if node.type == ASTType.ESE:
            return self.visitEse(node)
        
        if node.type == ASTType.ODO:
            return self.visitOdo(node)

    def translate(self, program: AST) -> str:
        translation = self.visit(program)

        return self.deifiedFunc +\
                self.reler +\
                translation