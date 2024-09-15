from argparse import ArgumentParser

from subprocess import run
from os.path import basename
from os.path import dirname

from reler.analysis.lexer import Lexer
from reler.analysis.parser import Parser
from reler.translator import Translator

class Cli:
    def __init__(self) -> None:
        self.lexer = Lexer()
        self.parser = Parser()
        self.translator = Translator()

        self.argParser = ArgumentParser()

        self.argParser.add_argument("sourcePath")
        self.argParser.add_argument("--execute", action = "store_true")

    def run(self):
        args = self.argParser.parse_args()

        translation = ""

        filename = basename(args.sourcePath)
        dist = dirname(args.sourcePath)

        with open(args.sourcePath) as file:
            buffer = file.read()
            stream = self.lexer.lex(buffer)
            ast = self.parser.parse(stream)
            translation = self.translator.translate(ast)

        outputPath = f"{dist}/{filename}.py"

        with open(outputPath, "w") as file:
            file.write(translation)

        print(f">>> [CLI] output in {outputPath}")

        if args.execute:
            print(f">>> [CLI] running {outputPath}:")
            run(["python", outputPath])
