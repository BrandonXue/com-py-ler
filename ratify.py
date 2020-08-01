# This program compiles Rat20SU code into p-code that is read by the rat.py
# virtual machine. The virtual machine uses a stack instead of registers.
# For usage information, including how to enter command-line arguments into
# this compiler, please see the README.md

import os.path
from sys import argv

from rat_parser import *
from rat_constants import *

def main():
    # Check to see how many arguments the user passed
    arg_count = len(argv)
    fname = ""
    infile_name = ""
    out_parse = ""
    out_code = ""

    lex_flag = False
    parse_flag = False
    code_flag = False
    ids_flag = False
    infile_taken = False
    for i in range(arg_count):
        # Find invalid flags and ignore them
        if argv[i].find("-") == 0 and argv[i] not in {"--lex", "--parse", "--ids", "-o"}:
            pass
        # Find the python script argument and ignore it
        elif argv[i].find(".py") != -1:
            pass
        # If the previous flag was -o, this argument will be treated as out_code name
        elif code_flag:
            out_code = argv[i]
            code_flag = False
        # If -lex flag detected, the program will create a .lex output
        elif argv[i] == "--lex":
            lex_flag = True
        # If -parse flag detected, the program will create a .parse output
        elif argv[i] == "--parse":
            parse_flag = True
        # If -ids flag is detected, the program will later print the symbol table to stdout
        elif argv[i] == "--ids":
            ids_flag = True
        # If -o flag detected, the next item will be treated as out_code name
        elif argv[i] == "-o":
            code_flag = True
            # If there is no next token, print error and exit
            if i+1 == arg_count:
                print("\tError: -o flag was activated but no file name followed.")
                exit()
        # Else no special conditions, that means this argument is the source file name
        elif not infile_taken:
            infile_taken = True
            infile_name = argv[i]
        else:
            print("\tError: Input filename detected twice. (Check if any flags are missing.)")
            exit()



    # ********** STEP ONE: **********
    # Handle the input file name

    # Make sure the user entered an input filename
    while infile_name == "":
        infile_name = input(
            "Input file name cannot be left blank. Enter the name of the source file: ")

    if not os.path.isfile(infile_name):
        print("\nError: The specified input file does not exist.\n")
        return

    # ********** STEP TWO: **********
    # Figure out all of the remaining file names and notify user

    # Find the file name without extension
    ext_index = infile_name.rfind(".")
    if ext_index == -1:
        fname = infile_name
    else:
        fname = infile_name[:ext_index]
    # Find the p-code output file name
    if out_code == "":
        out_code = fname + ".out"
    # Create the .parse output file name
    out_parse = fname + ".parse"
    # Create the .lex output file name
    out_lex = fname + ".lex"

    print("Input file:", infile_name)
    if lex_flag:
        print("Lexer output:", out_lex)
    if parse_flag:
        print("Parser output:", out_parse)
    print("P-code output:", out_code)

    # ********** STEP THREE: **********
    # Begin running the compilation process

    # Create a parser and give it flags and filenames
    rp = RatParser(infile_name, out_code, out_parse, out_lex, parse_flag, lex_flag)

    rp.rat20su() # Begin recursive descent parse

    rp.output_instr() # Output p-code

    rp.print_errors()
        
    if ids_flag: # if ids_flag is set, print the symbol table
        print()
        rp.print_ids()

    rp.close_files() # Close all files

if __name__ == "__main__":
    main()

