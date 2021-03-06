import re

program: list = []
memory: dict = {}
stack: list = []
flag: dict = {}
macro: dict = {}
macro_origin: int = 0
program_pointer: int = 0
blocking: bool = False
lookup_flag = ''


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
        val = str(val).replace("\\\\", " ")
        stack.append(str(val))


# Writes a value to memory. Uses last value as address and the value before
# that as value to write
# Syntax: memw
def op_memw():
    memory[get_from_stack()] = get_from_stack(1)


# Reads a value from memory. Uses last value as address and adds it on the stack
# Syntax: memr
def op_memr():
    stack.append(memory[get_from_stack()])


# Removes the value on top of the stack
# Syntax rm
def op_remove():
    stack.pop()


# Clears the whole stack. Syntax: clear
def op_clear():
    stack.clear()


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


# saves flags that occurred with jump value
def flag_save():
    flag[get_from_stack()] = program_pointer


# Jump to a flag when reached
# Syntax: jump
def flag_jump():
    global lookup_flag, blocking
    global lookup_flag, program_pointer, blocking
    if flag.__contains__(get_from_stack()):
        program_pointer = int(flag[get_from_stack()])
    else:
        lookup_flag = get_from_stack()
        blocking = True


# if conditions. First value 0: proceed, 1: jump. Second value: jump to
def cond_if():
    global lookup_flag, program_pointer, blocking
    if get_from_stack(1) == 1:
        if flag.__contains__(get_from_stack()):
            program_pointer = int(flag[get_from_stack()])
        else:
            lookup_flag = get_from_stack()
            blocking = True


# if conditions. First value 0: jump, 1: proceed. Second value: jump to flag
def cond_false_if():
    global lookup_flag, program_pointer, blocking
    if get_from_stack(1) == 0:
        if flag.__contains__(get_from_stack()):
            program_pointer = int(flag[get_from_stack()])
        else:
            lookup_flag = get_from_stack()
            blocking = True


# Swaps last value and value before that around
# Syntax: swap
def op_swap():
    save = get_from_stack()
    stack[len(stack) - 1] = stack[len(stack) - 2]
    stack[len(stack) - 2] = save


# creates a macro to make code more readable. similar to methods
def macro_save():
    global blocking
    macro[get_from_stack()] = program_pointer
    blocking = True


# the end keyword, to show that a macro is over
def macro_end():
    global program_pointer
    program_pointer = macro_origin


# checks if a macro is called and executes it
def macro_check(keyword: str):
    global macro_origin, program_pointer
    if macro.__contains__(keyword):
        macro_origin = program_pointer
        program_pointer = macro[keyword]
        return True
    return False


# Loads a user given input to the stack. The last value on stack will be used as prompt
# Syntax: in
def input_in():
    stack_write(input(get_from_stack()))
    pass


def check_for_operation(op: str):
    global program_pointer, blocking
    # blocking check
    if op == lookup_flag and blocking:
        if program[program_pointer + 1] == "flag":
            blocking = False
        program_pointer -= 1
    if op == "end" and blocking:
        blocking = False
        return
    if blocking:
        return

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
    elif op == "flag":
        flag_save()
    elif op == "jump":
        flag_jump()
    elif op == "if":
        cond_if()
    elif op == "!if":
        cond_false_if()
    # In/Output operation
    elif op == "out":
        op_out()
    elif op == "in":
        input_in()
    # Stack manipulator operation
    elif op == "swap":
        op_swap()
    elif op == "rm":
        op_remove()
    elif op == "clear":
        op_clear()
    # Memory manipulation operation
    elif op == "memw":
        op_memw()
    elif op == "memr":
        op_memr()
    # Macro check
    elif op == "macro":
        macro_save()
    elif op == "end":
        macro_end()
    # Stack value write
    else:
        if not macro_check(op):
            stack_write(op)


def pegasm_compile(code: list):
    global program_pointer, program
    split_in_ops(code)
    while program_pointer < len(program):
        check_for_operation(program[program_pointer])
        program_pointer += 1
