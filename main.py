import sys
from compiler.interpreter import pegasm_compile


def file_getter(path: str):
    with open(path) as file:
        content: str = file.read()
        file.close()
        return content


if __name__ == "__main__":
    arguments: list = sys.argv
    # get the file to execute
    pegasm_compile(file_getter(arguments[1]))
