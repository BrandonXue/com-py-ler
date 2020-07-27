# This is the Rat20SU virtual machine. Run the program and enter the
# p-code file as the command-line argument. If no command-line
# argument is provided, the program will prompt you.

import os.path
from sys import argv

Instructions = [
    ["LABEL", "nil"] # Instruction 0 is a filler to make indices equal to instr addr
]

Mem = {}

Stack = []

def err_exit(msg):
    print("\tError: " + msg + "\n")
    exit()

def execute_line(pc):
    # If the instruction has not been loaded yet, don't advance pc
    if pc >= len(Instructions):
        return pc

    # Find the instruction type and argument (if any)
    instr = Instructions[pc]
    instr_type = instr[0]
    instr_arg = ""
    if len(instr) > 1:
        instr_arg = instr[1]

    if instr_type == "PUSHI":
        if len(instr) < 2:
            err_exit("No arg for PUSHI at line " + str(pc))
        Stack.append(int(instr_arg))
        return pc + 1
    elif instr_type == "PUSHM":
        if len(instr) < 2:
            err_exit("No arg for PUSHM at line " + str(pc))
        if instr_arg not in Mem:
            err_exit("PUSHM on uninitialized memory location at line " + str(pc))
        Stack.append(Mem[instr_arg])
        return pc + 1
    elif instr_type == "POPM":
        if len(instr) < 2:
            err_exit("No arg for POPM at line " + str(pc))
        if len(Stack) == 0:
            err_exit("POPM on empty stack at line " + str(pc))
        num = Stack.pop()
        Mem[instr_arg] = num
        return pc + 1
    elif instr_type == "STDOUT":
        if len(Stack) == 0:
            err_exit("POPM on empty stack at line " + str(pc))
        num = Stack.pop()
        print(num)
        return pc + 1
    elif instr_type == "STDIN":
        num = int(input())
        Stack.append(num)
        return pc + 1
    elif instr_type == "ADD":
        num2 = Stack.pop()
        num1 = Stack.pop()
        Stack.append(num1 + num2)
        return pc + 1
    elif instr_type == "SUB":
        num2 = Stack.pop()
        num1 = Stack.pop()
        Stack.append(num1 - num2)
        return pc + 1
    elif instr_type == "MUL":
        num2 = Stack.pop()
        num1 = Stack.pop()
        Stack.append(num1 * num2)
        return pc + 1
    elif instr_type == "DIV":
        num2 = Stack.pop()
        num1 = Stack.pop()
        if num2 == 0:
            err_exit("Division by 0 at line " + str(pc))
        Stack.append(num1 // num2)
        return pc + 1
    elif instr_type == "GRT":
        num2 = Stack.pop()
        num1 = Stack.pop()
        res = 1 if num1 > num2 else 0
        Stack.append(res)
        return pc + 1
    elif instr_type == "LES":
        num2 = Stack.pop()
        num1 = Stack.pop()
        res = 1 if num1 < num2 else 0
        Stack.append(res)
        return pc + 1
    elif instr_type == "EQU":
        num2 = Stack.pop()
        num1 = Stack.pop()
        res = 1 if num1 == num2 else 0
        Stack.append(res)
        return pc + 1
    elif instr_type == "JUMPZ":
        if len(instr) < 2:
            err_exit("No arg for JUMPZ at line " + str(pc))
        num = Stack.pop() # Pop the stack
        if num == 0: # Jump if 0
            return int(instr_arg)
        elif num == 1: # Don't jump if 1
            return pc + 1
        else:
            err_exit("Stack top was not a boolean during JUMPZ at line" + str(pc))
    elif instr_type == "JUMP":
        if len(instr) < 2:
            err_exit("No arg for JUMP at line " + str(pc))
        return int(instr_arg)
    elif instr_type == "LABEL":
        return pc + 1
    else:
        err_exit("Unknown command at line " + str(pc))

# Takes a string representing one line of p-code
# Decodes the p-code and puts it into the list
# Return the instruction address/number
def load_instruction(line):
    instr = line.split()
    # Get rid of the instruction number, the list index will serve as instr number
    instr = instr[1:]
    Instructions.append(instr)
    # Return the instruction number that was just loaded
    return len(Instructions)-1

def run_program(p_code):
    pc = 1 # Program counter (in this case instr number)
    line = p_code.readline()
    while line != "":
        # Load the instruction and note the instruction number
        max_line = load_instruction(line)
        # While the desired instructions are available, run them
        while pc <= max_line:
            pc = execute_line(pc)
        line = p_code.readline()
    
    # pc should be equal to the length of Instructions at the end of execution

def main():
    # Check to see how many arguments the user passed
    arg_count = len(argv)
    p_code_name = ""

    # If there is a command-line argument provided
    # assume the second one is the file name
    if arg_count > 1:
        p_code_name = argv[1]

    # Make sure the user entered an input filename
    while p_code_name == "":
        p_code_name = input(
            "File name cannot be blank. Enter file name of a compiled Rat20SU program: ")

    if not os.path.isfile(p_code_name):
        print("\nError: The specified p-code file does not exist.\n")
        return

    p_code = open(p_code_name, "r")

    run_program(p_code)

    p_code.close()

if __name__ == "__main__":
    main()

