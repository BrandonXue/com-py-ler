## Introduction
A compiler for the Rat20SU language that creates p-code, and a Rat20SU virtual machine that recognizes said p-code.

## Usage Information
1. Python 3 is required to run this program.
    - The official Tuffix distribution should come with Python 3.
    - To check if you have Python 3, open your terminal emulator and follow the instructions for your OS.
        - Tuffix/Linux: python3 --version
        - Windows: py --version

2. Make sure all necessary files are present in the same project directory.
   Only the "Required files" and "Input files" are needed to test the program.
   Here is a list of all the files:
    - "Required files" to run the program:
	- ratify.py		----	the main script file
        - lexer_constants.py	----	set definitions & constants
        - rat_lexer.py		----	the RatLexer & Token classes
	- rat_parser.py		----	the RatParser class
	- reader.py		----	a wrapper class for file input

    - "Input files" for testing the program:
        - test1.rat        ----    test file 1, <10 lines
        - test2.rat        ----    test file 2, <20 lines
        - test3.rat        ----    test file 3, >20 lines

    - "Output files" for the given input files:
        - test1.out        ----    p-code for test1.rat
        - test2.out        ----    p-code for test2.rat
        - test3.out        ----    p-code for test3.rat

3. Navigate your terminal emulator to the directory containing the project files.
    - Tuffix/Linux: cd ...path/to/project/directory
    - Windows: cd ...path\to\project\directory 

4. Using Python3, Run the main script file Ratify.py.
    - Run the program and specify the input file. If not specified, the program will prompt you once it starts running.
    - Optionally provide a "-o" flag and then type the output filename as the next argument.
    - Optionally provide a "-ids" flag to print the symbol table to stdout
    - Optionally provide a "-lex" flag to print a .lex output file
    - Optionally provide a "-parse" flag to print a .parse output file

    - Tuffix/Linux: python3 Ratify.py test1.txt myoutput.txt
    - Windows: py -3 Ratify.py test1.txt myoutput.txt

    - If no command line arguments are given, the program will prompt you for file names. Please follow the command prompt.
    - The input file must match your source code file name. The output file must also be provided. For the output file name, be careful not to use the name of an existing file, otherwise its contents will be replaced. 


## Collaborators
Brandon Xue, Henry Torres, Miguel Pulido