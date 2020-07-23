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
    # If the user passed at least one, use the first one as the file
    # of the source code to be processed. If the user passed at least two,
    # use the second one as the name of the output file to be generated
    cli_args = len(argv)
    infile_name = ""
    outfile_name = ""

    # ********** STEP ONE: **********
    # Handle the input file name
    if cli_args < 2:
        infile_name = input("Enter the name of the source file: ")
    else:
        infile_name = argv[1]
    # Verify that the input file exists
    if infile_name == "":
        print("\nError: No file name was entered.\n")
        return
    if not os.path.isfile(infile_name):
        print("\nError: The specified input file does not exist.\n")
        return

    # ********** STEP TWO: **********
    # Handle the output file name
    if cli_args < 3:
        msg = "Enter the name of the output file"
        outfile_name = input(msg + ": ")
        while outfile_name == "":
            outfile_name = input("Output file name cannot be left blank. " + msg + ": ")
    else:
        outfile_name = argv[2]

    # Create a parser and give it the source file name so it can
    # pass the file to the lexer, and give it the output file name
    rp = RatParser(infile_name, outfile_name)

    rp.rat20su()

    rp.close_files()

if __name__ == "__main__":
    main()

