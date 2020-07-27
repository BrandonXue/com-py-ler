## Introduction
A compiler for the Rat20SU language that uses a table-driven DFA lexer and recursive descent parsing as the front end.
The compiler creates p-code for a virtual machine (rat.py).

## Usage Information
1. Python 3 is required to run this program.
    - The official Tuffix (Tuffy the Titan's Linux) distribution should come with Python 3.
    - To check if you have Python 3, open your terminal emulator and follow the instructions for your OS.
        - Tuffix/Linux: python3 --version
        - Windows: py --version

2. Make sure all necessary files are present in the same project directory.
   Only the "Required files" and "Input files" are needed to test the program.
   Here is a list of all the files:
    - "Required files" to run the program:
        - ratify.py		        ----	the main script file for the compiler
        - lexer_constants.py	----	set definitions & constants
        - rat_lexer.py		    ----	the RatLexer & Token classes
        - rat_parser.py		    ----	the RatParser class
        - reader.py		        ----	a wrapper class for file input

    - Virtual machine:
        - rat.py                ----    a virtual machine to recognize compiled p-code

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
    - Run the program and specify the input file.
    - If command line arguments are not given, the program will prompt you once it starts running. In this case, please follow the command prompt.
    - By default, the output filename will be the same as the input, but with a .out file extension.
        - Optionally provide a "-o" flag and then type the output filename as the next argument.
        - Optionally provide a "-ids" flag to print the symbol table to stdout
        - Optionally provide a "-lex" flag to create a .lex output file
        - Optionally provide a "-parse" flag to create a .parse output file

    - Tuffix/Linux: python3 ratify.py test1.rat -ids -o test1.out
    - Windows: py -3 ratify.py test1.rat -ids -o test1.out
    
    - To get all the outputs, try the following:
        - Tuffix/Linux: python3 ratify.py test1.rat -ids -lex -parse
        - Windows: py -3 ratify.py test1.rat -ids -lex -parse


## Collaborators
Brandon Xue, Henry Torres, Miguel Pulido
