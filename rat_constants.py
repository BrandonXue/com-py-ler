## =====================================================================================
##    LEXER
## =====================================================================================

# Token types are stored as integers to save memory.
# This can be thought of as an enum.
TokenComment    = 0
TokenIdentifier = 1
TokenInteger    = 2
TokenInvalid    = 3
TokenKeyword    = 4
TokenOperator   = 5
TokenSeparator  = 6

# The string representation of a token can be found by accessing this array
# at the index indicated by the value above.
TokenTypeStr = [
    'Comment', 'Identifier', 'Integer', 'Invalid',
    'Keyword', 'Operator', 'Separator'
]

# The following sets categorize some of the characters of the Rat20SU language
#
# Note that asterisk and equal sign are intentionally excluded from operators.
# This is because characters can only be grouped together if they are
# functionally equivalent. Equal sign is used as = or ==, so it cannot be
# handled the same way as single-char operators. Asterisks are used in comments
# so they are not functionally equivalent either.
#
# Note that brackets [] are intentionally excluded from separators. This is because
# Rat20SU does not support array operators. The only time brackets are used is for
# comments.
Whitespaces = {" ", "\t", "\n"}
Operators = {"+", "-", "/", ">", "<"}
Separators = {";", "(", ")", "{", "}"}
Keywords = {
    "integer", "int", "boolean", "bool", "true", "false",
    "if", "otherwise", "fi", "while", "get", "put"
}

# Distinguishing characters signal the start of a new token
# if we are on an accepting state for identifiers or integers
Distinguishing = {"*", "=", "["}.union(Whitespaces).union(Operators).union(Separators)


## =====================================================================================
##    PARSER and SYNTAX DIRECTED TRANSLATION
## =====================================================================================

PRINT_TOKENS = True
PRINT_PRODUCTIONS = True

INTEGER_T = 0
BOOLEAN_T = 1
NONE_T = 2

# Used these constants to encode the instruction type
# as an integer instead of string to save space
PUSHI = 1
PUSHM = 2
POPM = 3
STDOUT = 4
STDIN = 5
ADD = 6
SUB = 7
MUL = 8
DIV = 9
GRT = 10
LES = 11
EQU = 12
JUMPZ = 13
JUMP = 14
LABEL = 15

# Use this dict to decode instruction types into a string
# so that the correct output can be printed
INSTR_TYPE = [
    "INVALID",
    "PUSHI", # I1
    "PUSHM", # I2
    "POPM",  # I3
    "STDOUT",# I4
    "STDIN", # I5
    "ADD",   # I6
    "SUB",   # I7
    "MUL",   # I8
    "DIV",   # I9
    "GRT",   # I10
    "LES",   # I11
    "EQU",   # I12
    "JUMPZ", # I13
    "JUMP",  # I14
    "LABEL"  # I15
]