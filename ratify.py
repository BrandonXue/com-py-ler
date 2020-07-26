# This program gets takes an optional command line argument.
# The argument should be the file name of a Rat20SU source code file.
# If no command line argument is received, the user will be prompted
# for a file name instead
#
# This is the first component of the Rat20SU programming language compiler.

import os.path
from sys import argv

from rat_parser import *
from lexer_constants import *

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
    for i in range(1, arg_count): # Starting from index 1 omits the script filename itself
        # If the previous flag was -o, this argument will be treated as out_code name
        if code_flag:
            out_code = argv[i]
            code_flag = False
        # If -lex flag detected, the program will create a .lex output
        elif argv[i] == "-lex":
            lex_flag = True
        # If -parse flag detected, the program will create a .parse output
        elif argv[i] == "-parse":
            parse_flag = True
        # If -id flag is detected, the program will later print the symbol table to stdout
        elif argv[i] == "-id":
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
            print("\tError: Input filename specified twice. Check if any flags are missing.")
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
    # Figure out all of the remaining file names

    # Find the file name without extension
    ext_index = infile_name.rfind(".")
    fname = infile_name[:ext_index]
    # Find the p-code output file name
    if out_code == "":
        out_code = fname + ".out"
    # Create the .parse output file name
    out_parse = fname + ".parse"
    # Create the .lex output file name
    out_lex = fname + ".lex"



    # ********** STEP THREE: **********
    # Begin running the compilation process

    # Create a parser and give it flags and filenames
    rp = RatParser(infile_name, out_code, out_parse, out_lex, parse_flag, lex_flag)

    rp.rat20su() # Begin recursive descent parse

    rp.output_instr() # Output p-code

    if ids_flag: # if ids_flag is set, print the symbol table
        rp.print_ids()

    rp.close_files() # Close all files

if __name__ == "__main__":
    main()

