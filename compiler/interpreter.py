import re

program: list = []
memory: list = []
stack: list = []
program_pointer: int = 0


# Get top of stack, value is offset. No value means top
def get_from_stack(offset: int = 0):
    return stack[(len(stack) - 1) - offset]


def is_int(val: str):
    try:
        int(val)
        return True
    except ValueError:
        return False


def is_float(val: str):
    try:
        float(val)
        return True
    except ValueError:
        return False


# Splits the program into its params
def split_in_ops(code: str):
    global program
    # remove unnecessary spaces and comment lines
    while code.__contains__('#'):
        code = code.replace(code[code.find('#'):code.find('\n') + 1], '')
    code = ' '.join(code.split())
    # Split code into parts
    program = re.compile("[\n ]").split(code)


# Writes a value to the stack. Syntax just value
def stack_write(val):
    if is_int(val):
        stack.append(int(val))
    elif is_float(val):
        stack.append(float(val))
    else:
        stack.append(str(val))


# Outputs top of stack. Syntax: out
def op_out():
    print(get_from_stack())


# Adds the last to values on the stack together and adds it on top of the stack
# Syntax: +
def calc_plus():
    stack_write(get_from_stack(1) + get_from_stack())


def check_for_operation(op: str):
    if op == '+':
        calc_plus()
    elif op == "out":
        op_out()
    else:
        stack_write(op)


def pegasm_compile(code: str):
    global program_pointer, program
    split_in_ops(code)
    while program_pointer < len(program):
        check_for_operation(program[program_pointer])
        program_pointer += 1
