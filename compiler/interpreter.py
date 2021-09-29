import re

program: list = []
memory: dict = {}
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


def is_float(val):
    val = str(val)
    try:
        if val.__contains__('.'):
            float(val)
            return True
        else:
            return False
    except ValueError:
        return False


# Splits the program into its params
def split_in_ops(line_code: list):
    global program
    # remove unnecessary spaces and comment lines
    for string in line_code[:]:
        if string[0] == '#':
            line_code.remove(string)
    code = ' '.join(line_code)
    code = ' '.join(code.split())
    # Split code into parts
    program = re.compile("[\n ]").split(code)


# Writes a value to the stack. Syntax just value
def stack_write(val):
    if is_float(val):
        stack.append(float(val))
    elif is_int(val):
        stack.append(int(val))
    else:
        stack.append(str(val))


# Writes a value to memory. Uses last value as address and the value before
# that as value to write
# Syntax: memw
def op_memw():
    memory[int(get_from_stack())] = get_from_stack(1)


# Reads a value from memory. Uses last value as address and adds it on the stack
# Syntax: memr
def op_memr():
    stack.append(memory[int(get_from_stack())])


# Removes the value on top of the stack
# Syntax rm
def op_remove():
    stack.pop()


# Outputs top of stack. Syntax: out
def op_out():
    print(get_from_stack())


# Adds the last two values on the stack together and adds it on top of the stack
# Syntax: +
def calc_plus():
    stack_write(get_from_stack(1) + get_from_stack())


# Subtracts the last two values on the stack and adds it to the stack
# Syntax -
def calc_minus():
    stack_write(get_from_stack(1) - get_from_stack())


# Multiplies the last two values and adds it on the stack
# Syntax *
def calc_multiply():
    stack_write(get_from_stack(1) * get_from_stack())


# Divides the last two values and adds it on the stack
# Syntax /
def calc_divide():
    stack_write(get_from_stack(1) / get_from_stack())


# Builds the modulo of the last two values and adds it on the stack
# Syntax %
def calc_modulo():
    stack_write(get_from_stack(1) % get_from_stack())


# does the conditional operations
# Syntax: <, >, =, <=, >=
def cond_less():
    stack.append(1 if get_from_stack(1) < get_from_stack() else 0)


def cond_more():
    stack.append(1 if get_from_stack(1) > get_from_stack() else 0)


def cond_equals():
    stack.append(1 if get_from_stack(1) == get_from_stack() else 0)


def cond_less_equal():
    stack.append(1 if get_from_stack(1) <= get_from_stack() else 0)


def cond_more_equal():
    stack.append(1 if get_from_stack(1) >= get_from_stack() else 0)


# Swaps last value and value before that around
# Syntax: swap
def op_swap():
    save = get_from_stack()
    stack[len(stack) - 1] = stack[len(stack) - 2]
    stack[len(stack) - 2] = save


def check_for_operation(op: str):
    # Math operation
    if op == '+':
        calc_plus()
    elif op == '-':
        calc_minus()
    elif op == '*':
        calc_multiply()
    elif op == '/':
        calc_divide()
    elif op == '%':
        calc_modulo()
    # Condition operation
    elif op == "<":
        cond_less()
    elif op == ">":
        cond_more()
    elif op == "=":
        cond_equals()
    elif op == "<=":
        cond_less_equal()
    elif op == ">=":
        cond_more_equal()
    # Output operation
    elif op == "out":
        op_out()
    # Stack manipulator operation
    elif op == "swap":
        op_swap()
    elif op == "rm":
        op_remove()
    # memory manipulation operation
    elif op == "memw":
        op_memw()
    elif op == "memr":
        op_memr()
    # Stack value write
    else:
        stack_write(op)


def pegasm_compile(code: list):
    global program_pointer, program
    split_in_ops(code)
    while program_pointer < len(program):
        check_for_operation(program[program_pointer])
        program_pointer += 1
