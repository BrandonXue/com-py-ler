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