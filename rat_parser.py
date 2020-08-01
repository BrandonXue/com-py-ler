from rat_constants import *
from rat_lexer import *

class RatParser:
    # Constructor
    # Takes two file names, one for the source and one for the output.
    # The source file name will be passed to the RatLexer
    def __init__(self, infile_name, out_code, out_parse, out_lex, parse_flag, lex_flag):
        # Prepare parsing output
        self.parse_flag = parse_flag
        if (PRINT_PRODUCTIONS or PRINT_TOKENS) and parse_flag:
            self.out_parse = open(out_parse, "w")

        # Prepare symbol table
        self.id_mem_addr = 5000
        self.sym_table = {}

        # Prepare jump stack
        self.jumpstack = []

        # Prepare ICG output
        self.out_code = open(out_code, "w")
        self.instructions = []
        self.instr_addr = 1

        # Prepare input
        self.la = RatLexer(infile_name, out_lex, lex_flag)
        self.token = None
        self.prev_token = None
        self.lexer()

        # Prepare Error Log
        self.errors = []
    
    # Enter panic mode and seek the given synchronizing token.
    # If skip is True, the sync token is discarded.
    # Any invalid tokens encountered will have an error reported.
    def panic_seek(self, sync_set, skip=False, identifier=False):
        if self.token == None:
            exit()
        print(sync_set)
        while True:
            if self.token.value in sync_set:
                break
            if self.token.type == TokenIdentifier and identifier:
                break
            self.lexer()
            if self.token.type == TokenInvalid:
                self.notify_error("Error: Invalid token", self.token)

        if skip:
            self.lexer()

    # Adds an error and/or a token to the error log
    def notify_error(self, msg="", token=None):
        self.errors.append((msg, token))

    # Special error message for missing semicolons. Must pass prev_token as argument
    def error_semicolon(self, token):
        col = token.char + len(token.value)
        msg = f"Error: Expected semicolon (;) at line {token.line} col {col}."
        self.errors.append((msg, None))

    # Print all errors in the log, if any
    def print_errors(self):
        for err in self.errors:
            print("\t" + err[0])
            if err[1] != None:
                print("\t" + err[1].__repr__())
            print()

    # Close both the input and output files.
    def close_files(self):
        if (PRINT_PRODUCTIONS or PRINT_TOKENS) and self.parse_flag:
            self.out_parse.close()
        self.out_code.close()
        self.la.close()


    ## =====================================================================================
    ##    The following functions help produce outputs for the parsing process only.
    ## =====================================================================================

    # A helper function that calls the RatLexer's lexer() and stores
    # the Token result as an instance variable. If there are no Tokens
    # left, and error will be printed and the program will exit.
    # 
    # The Token type and lexeme will be printed to the output if 
    # PRINT_TOKENS is set to True
    def lexer(self):
        self.prev_token = self.token
        self.token = self.la.lexer()
        if not self.token:
            print("\tError: Ran out of tokens.")
            exit()
        if PRINT_TOKENS and self.parse_flag:
            self.write_token()

    # Writes the current Token held by the RatParser into the output
    # file. This will write both the token type and the lexeme.
    # If there is no Token currently held by the RatParser, an error
    # will be printed and the program will exit.
    def write_token(self):
        if not self.token:
            print("\tError: No token available.")
            exit()
        type_str = TokenTypeStr[self.token.type]
        self.out_parse.write(f"Token: {type_str}".ljust(20) + f"Lexeme: {self.token.value}\n")

    # Write a string to the output file. The string will be indented
    # by four spaces.
    #
    # If PRINT_PRODUCTIONS is False, this function will do nothing.
    def write_production(self, string):
        if PRINT_PRODUCTIONS and self.parse_flag:
            self.out_parse.write("    " + string + "\n")


    ## =====================================================================================
    ##    The following functions are used to aid intermediate code generation.
    ## =====================================================================================

    # Check if an id is already inside the table
    def is_id(self, id):
        return id in self.sym_table

    # Make a declaration for an identifier
    def decl_id(self, id, id_type):
        if self.is_id(id):
            return False
        self.sym_table[id] = (self.id_mem_addr, id_type)
        self.id_mem_addr += 1
        return True

    # Return the address of the identifier if in the table, otherwise return -1
    def get_address(self, id):
        if self.is_id(id):
            return self.sym_table[id][0]
        return -1

    # Takes an identifier and returns its type as an integer
    def get_type(self, id):
        if self.is_id(id):
            return self.sym_table[id][1]
        return -1

    # Print all the identifiers in the table
    def print_ids(self):
        print("Identifier".ljust(15) + "Memory Location".ljust(20) + "Type")
        print("".ljust(42, "-"))
        for id in self.sym_table:
            id_str = f"{id}".ljust(15)
            loc_str = f"{self.sym_table[id][0]}".ljust(20)
            type_str = "boolean" if self.sym_table[id][1] else "integer"
            print(id_str + loc_str + type_str)

    # Generate an output instruction line
    def gen_instr(self, instr_type, arg):
        if self.instr_addr >= 5000:
            print("\tError: Instruction reached addr 5000")
            exit()
        new_instr = [self.instr_addr, instr_type, arg]
        self.instructions.append(new_instr)
        self.instr_addr += 1

    # Add an instruction address to the jumpstack
    # This is typically an instruction that later needs to be supplied an argument
    def push_jumpstack(self, addr):
        self.jumpstack.append(addr)

    # Add an argument to a previous instruction
    # This is necessary because sometimes we don't know the jump address.
    # For example if an if-statement condition is false, we don't know
    # how mant instructions are in the statement and where to jump past.
    def back_patch(self, jump_addr):
        instr_addr = self.jumpstack.pop()
        # Since indices start at 0 but instructions start at 1
        # we must subtract 1 to access the instruction at the given address
        # Instructions are a 3-item list, so the arg is stored at index 2
        self.instructions[instr_addr-1][2] = jump_addr

    # Output all the instructions to the output file out_code
    def output_instr(self):
        for instr in self.instructions:
            self.out_code.write(str(instr[0]).ljust(6))
            instr_str = INSTR_TYPE[instr[1]]
            self.out_code.write(instr_str.ljust(10))
            arg = str(instr[2])
            if arg != "nil":
                self.out_code.write(str(instr[2]))
            self.out_code.write("\n")
            

    ## =====================================================================================
    ##    The following functions represent the rules of the Rat20SU language.
    ##    Each function handles the productions of one nonterminal.
    ##    The functions will print messages to an output file if the respective
    ##    print flags are set to True.
    ## =====================================================================================



    # <Rat20SU>
    # (STARTING SYMBOL)
    # This function should be called first to begin predictive recursive descent.
    def rat20su(self):
        if self.token.value == "$$":
            self.write_production("<Rat20SU> -> $$ <Opt Declaration List> <Statement List> $$")
            self.lexer()
        elif self.token.type == TokenInvalid:
            self.notify_error("Error: Invalid token, expected $$", self.token)
            self.lexer()
        else: # If $$ not provided, assume the user forgot, notify error, and continue
            self.notify_error("Error: Expected $$", self.token)

        self.opt_declaration_list()
        self.statement_list()

        if self.token.value == "$$":
            if len(self.errors) == 0:
                self.write_production("\nRat20SU Accepted")
            else:
                self.write_production("\n!!! Parsed With Errors !!!")
        elif self.token.type == TokenInvalid:
            self.notify_error("Error: Invalid token, expected $$", self.token)
        else: # If $$ not provided, assume the user forgot, notify error, and continue
            self.notify_error("Error: Expected $$", self.token)

    # <Opt Declaration List>
    def opt_declaration_list(self):
        if self.token.value in {"integer", "boolean"}:
            self.write_production("<Opt Declaration List> -> <Declaration List>")
            self.declaration_list()
        else:
            self.write_production("<Opt Declaration List> -> <Empty>")
            # Since the production for <Empty> is trivial, it will not
            # be given its own function.
            self.write_production("<Empty> -> epsilon")

    # <Declaration List>
    def declaration_list(self):
        if self.token.value in {"integer", "boolean"}:
            self.write_production("<Declaration List> -> <Declaration> ; <Declaration List Split>")
            try:
                self.declaration()
            except: # Panic mode to ;
                self.panic_seek({";"}, skip=False)

            if self.token.value != ";":
                self.error_semicolon(self.prev_token)
            else: # If no semicolon, assume the user forgot it and continue.
                self.lexer()

            self.declaration_list_split()
        else:
            self.notify_error("Bug: declaration_list()")

    # <Declaration>
    def declaration(self):
        if self.token.value in {"integer", "boolean"}:
            self.write_production("<Declaration> -> <Qualifier> <Identifier>")
            tok_type = self.qualifier()
            if self.token.type == TokenIdentifier:
                tok_id = self.token.value
                if tok_id != NONE_T:
                    self.decl_id(tok_id, tok_type)
                self.lexer()
            else:
                self.notify_error("Error: Expected identifier", self.token)
                raise Exception()
        else:
            self.notify_error("Bug: declaration()")

    # <Qualifier>
    def qualifier(self):
        if self.token.value == "integer":
            self.write_production("<Qualifier> -> integer")
            self.lexer()
            return INTEGER_T
        elif self.token.value == "boolean":
            self.write_production("<Qualifier> -> boolean")
            self.lexer()
            return BOOLEAN_T
        else:
            self.notify_error("Bug: qualifier()") # shouldn't be reachable
            return NONE_T

    # <Declaration List Split>
    # This rule comes from factoring <Declaration List>
    def declaration_list_split(self):
        if self.token.value in {"integer", "boolean"}:
            self.write_production("<Declaration List Split> -> <Declaration List>")
            self.declaration_list()
        else:
            self.write_production("<Declaration List Split> -> epsilon")

    # <Statement List>
    def statement_list(self):
        if self.token.value in {
            "if", "while", "get", "put", "{"
            } or self.token.type == TokenIdentifier:
            self.write_production("<Statement List> -> <Statement> <Statement List Split>")
 
        # Even if there is an error, proceed and let panic mode handle it.
        try:
            self.statement()
        except:
            self.panic_seek({";", "}", "$", "$$", "$$$"}, skip=False)
            if self.token.value == ";":
                self.lexer()
        self.statement_list_split()

    # <Statement>
    def statement(self):
        if self.token.value == "{":
            self.write_production("<Statement> -> <Compound>")
            try:
                self.compound()
            except:
                self.panic_seek({"}"}, skip=True)
        elif self.token.type == TokenIdentifier:
            self.write_production("<Statement> -> <Assign>")
            try:
                self.assign()
            except:
                self.panic_seek({"}"}, skip=True)
        elif self.token.value == "if":
            self.write_production("<Statement> -> <If>")
            try:
                self.if_rule()
            except:
                self.panic_seek("fi", skip=True)
        elif self.token.value == "put":
            self.write_production("<Statement> -> <Put>")
            try:
                self.put()
            except:
                self.panic_seek({";"}, skip=True)
        elif self.token.value == "get":
            self.write_production("<Statement> -> <Get>")
            try:
                self.get()
            except:
                self.panic_seek({";"}, skip=True)
        elif self.token.value == "while":
            self.write_production("<Statement> -> <While>")
            self.while_rule()
        elif self.token.value in {"integer", "boolean"}:
            self.notify_error("Error: Declaration not allowed in statement block", self.token)
            raise Exception()
        else:
            self.notify_error("Error: Unexpected token or start of statement", self.token)
            raise Exception()

    # <Statement List Split>
    # This rule comes from factoring <Statement List>
    def statement_list_split(self):
        # If we encounter Follow(Statement_List_Split), then this goes to epsilon
        if self.token.value in {"}", "$", "$$", "$$$"}: # Account for typos
            self.write_production("<Statement List Split> -> epsilon")
        else: # For all other lexemes, let statement_list handle it. Errors handled with panic mode
            self.write_production("<Statement List Split> -> <Statement List>")
            self.statement_list()

    # <Compound>
    def compound(self):
        if self.token.value == "{":
            self.write_production("<Compound> -> { <Statement List> }")
            self.lexer()
            self.statement_list()
            if self.token.value != "}":
                self.notify_error("Error: Expected }", self.token)
                raise Exception()
            else: 
                self.lexer()
        else:
            self.notify_error("Bug: compound()")

    # <Assign>
    def assign(self):
        if self.token.type == TokenIdentifier:
            tok = self.token
            addr = self.get_address(tok.value)
            self.write_production("<Assign> -> <Identifier> = <Expression> ;")
            self.lexer()
            eq_sign = self.token
            if self.token.value == "=":
                self.lexer()
                expr_type = self.expression()

                # Type check assignment
                id_type = self.get_type(tok.value)
                if id_type != expr_type:
                    self.notify_error(
                        "Error: cannot assign " + VarTypes[expr_type] + " to " + VarTypes[id_type],
                        eq_sign)

                # Check for semicolon. If no semicolon, assume the user forgot it and continue.
                if self.token.value != ";":
                    self.error_semicolon(self.prev_token)
                else:
                    self.lexer()

                if addr == -1:
                    self.notify_error("Error: Use of undeclared identifier", tok)
                self.gen_instr(POPM, addr)
            elif addr == -1: # if no equal sign and address is invalid, assume the user didn't mean to make assignment
                self.notify_error("Error: Unexpected token or start of statement", self.token)
                raise Exception()
            else:
                self.notify_error("Error: Expected =", self.token)
                raise Exception()
        else:
            self.notify_error("Bug: assign()")

    # <If>
    def if_rule(self):
        if self.token.value == "if":
            self.write_production("<If> -> if ( <Condition> ) <Statement> <If Split>")
            self.lexer()
            if self.token.value == "(":
                self.lexer()
                self.condition()
                if self.token.value == ")":
                    self.lexer()
                    self.statement()
                    # Store the address of this jump, it will be used for the "then" to jump past "else"
                    addr = self.instr_addr
                    self.gen_instr(JUMP, "nil")

                    self.back_patch(self.instr_addr) # If the condition fails, it will jump to here
                    # This is either the end of the if-statement, or the beginning of the "else" part
                    self.gen_instr(LABEL, "nil")
                    self.if_split()

                    # This is the end of the if-statement. We need to jump here from the end of "then"
                    # This may be redundant if there was no "else", but that's okay. There is room for
                    # improvement because we can get rid of potential redundancies.
                    self.push_jumpstack(addr) # Add that previous jump to jumpstack
                    self.back_patch(self.instr_addr) # back_patch it with the following label
                    self.gen_instr(LABEL, "nil")
                else:
                    self.notify_error("Error: Expected )", self.token)
                    raise Exception()
            else:
                self.notify_error("Error: Expected (", self.token)
                raise Exception()
        else:
            self.notify_error("Bug: if_rule()")

    # <If_Split>
    # This rule comes from factoring <If>
    def if_split(self):
        if self.token.value == "fi":
            self.write_production("<If Split> -> fi")
            self.lexer()
        elif self.token.value == "otherwise":
            self.write_production("<If Split> -> otherwise <Statement> fi")
            self.lexer()
            self.statement()
            if self.token.value == "fi":
                self.lexer()
            else:
                self.notify_error("Error: Expected fi", self.token)
                raise Exception()
        else:
            self.notify_error("Error: Expected fi or otherwise", self.token)
            raise Exception()
    
    # <While>
    def while_rule(self):
        if self.token.value == "while":
            self.write_production("<While> -> while ( <Condition> ) <Statement>")
            self.lexer()
            instr_addr = self.instr_addr
            self.gen_instr(LABEL, "nil")

            if self.token.value == "(":
                self.lexer()
            else: # If there is an error, assume the user forgot the ( and continue
                self.notify_error("Expected (", self.token)

            try: # If there is an error with the condition, panic mode to the closing parentheses
                self.condition()
            except:
                self.panic_seek({")"}, skip=False)

            if self.token.value == ")":
                self.lexer()
            else: # If there is an error, continue directly to the statement
                self.notify_error("Expected )", self.token)
                self.panic_seek({"if", "while", "{", "get", "put"}, skip=False, identifier=True)

            self.statement()
            # The loop will always jump back to the label just before the condition
            self.gen_instr(JUMP, instr_addr)
            # If the condition fails, it will jump to the label
            self.back_patch(self.instr_addr)
            self.gen_instr(LABEL, "nil")
        else:
            self.notify_error("Bug: while_rule()")

    # <Condition>
    def condition(self):
        if self.token.value in {
            "true", "false", "(", "-"
            } or self.token.type == TokenIdentifier or self.token.type == TokenInteger:
            self.write_production("<Condition> -> <Expression> <Relop> <Expression>")
            l_type = self.expression()
            op, op_token = self.relop()
            r_type = self.expression()

            # Type check comparison
            if l_type != r_type:
                self.notify_error(
                    "Error: Cannot compare " + VarTypes[l_type] + " with " + VarTypes[r_type],
                    op_token
                )
            elif l_type == BOOLEAN_T and op in {GRT, LES}:
                self.notify_error(
                    "Error: Cannot perform " + op_token.value + " operation on booleans",
                    op_token
                )

            self.gen_instr(op, "nil")
            self.push_jumpstack(self.instr_addr)
            self.gen_instr(JUMPZ, "nil")
        else:
            self.notify_error("Error: Expected start of expression", self.token)
            raise Exception()

    # <Relop>
    def relop(self):
        op_token = self.token
        if self.token.value == "==":
            self.write_production("<Relop> -> ==")
            self.lexer()
            return (EQU, op_token)
        elif self.token.value == ">":
            self.write_production("<Relop> -> >")
            self.lexer()
            return (GRT, op_token)
        elif self.token.value == "<":
            self.write_production("<Relop> -> <")
            self.lexer()
            return (LES, op_token)
        else:
            self.notify_error("Error: Expected relop", self.token)
            # If there's an error, return LABEL to signify error
            return (LABEL, op_token)

    # <Put>
    def put(self):
        if self.token.value == "put":
            self.write_production("<Put> -> put ( <Identifier> ) ;")
            self.lexer()
            if self.token.value == "(":
                self.lexer()
                tok = self.token
                if self.token.type == TokenIdentifier:
                    self.lexer()
                    if self.token.value == ")":
                        self.lexer()
                        # Check for semicolon. If no semicolon, assume the user forgot it and continue.
                        if self.token.value != ";":
                            self.error_semicolon(self.prev_token)
                        else:
                            self.lexer()
                        addr = self.get_address(tok.value)
                        if addr == -1:
                            self.notify_error("Error: Use of undeclared identifier", tok)
                        self.gen_instr(PUSHM, addr)
                        self.gen_instr(STDOUT, "nil")
                    else:
                        self.notify_error("Error: Expected )", self.token)
                        raise Exception()
                else:
                    self.notify_error("Error: Expected identifier", self.token)
                    raise Exception()
            else:
                self.notify_error("Error: Expected (", self.token)
                raise Exception()
        else:
            self.notify_error("Bug: put")

    # <Get>
    def get(self):
        if self.token.value == "get":
            self.write_production("<Get> -> get ( <Identifier> ) ;")
            self.lexer()
            if self.token.value == "(":
                self.lexer()
                tok = self.token
                if self.token.type == TokenIdentifier:
                    self.lexer()
                    if self.token.value == ")":
                        self.lexer()
                        # Check for semicolon. If no semicolon, assume the user forgot it and continue.
                        if self.token.value != ";":
                            self.error_semicolon(self.prev_token)
                        else:
                            self.lexer()
                        addr = self.get_address(tok.value)
                        if addr == -1:
                            self.notify_error("Error: Use of undeclared identifier", tok)
                        self.gen_instr(STDIN, "nil")
                        self.gen_instr(POPM, addr)
                    else:
                        self.notify_error("Error: Expected )", self.token)
                        raise Exception()
                else:
                    self.notify_error("Error: Expected identifier", self.token)
                    raise Exception()
            else:
                self.notify_error("Error: Expected (", self.token)
                raise Exception()
        else:
            self.notify_error("Bug: get")

    # <Expression>
    def expression(self):
        if self.token.value in {
            "false", "(", "-", "true"
            } or self.token.type == TokenIdentifier or self.token.type == TokenInteger:
            self.write_production("<Expression> -> <Term> <Expression Prime>")
            term_type = self.term()
            self.expression_prime(term_type)
            return term_type
        else:
            self.notify_error("Error: Invalid token", self.token)
            raise Exception()

    # <Expression Prime>
    # This rule comes from fixing the direct left recursion of <Expression>
    def expression_prime(self, prev_term_type):
        tok = self.token
        if self.token.value == "+":
            self.write_production("<Expression Prime> -> + <Term> <Expression Prime>")
            self.lexer()
            term_type = self.term()

            # Type check addition
            if term_type == BOOLEAN_T or prev_term_type == BOOLEAN_T:
                self.notify_error("Error: Cannot add booleans", tok)

            self.gen_instr(ADD, "nil")
            self.expression_prime(term_type)
            return term_type
        elif self.token.value == "-":
            self.write_production("<Expression Prime> -> - <Term> <Expression Prime>")
            self.lexer()
            term_type = self.term()

            # Type check subtraction
            if term_type == BOOLEAN_T or prev_term_type == BOOLEAN_T:
                self.notify_error("Error: Cannot subtract booleans", tok)

            self.gen_instr(SUB, "nil")
            self.expression_prime(term_type)
            return term_type
        else:
            self.write_production("<Expression Prime> -> epsilon")
            return NONE_T

    # <Term>
    def term(self):
        if self.token.value in {
            "true", "false", "(", "-"
            } or self.token.type == TokenIdentifier or self.token.type == TokenInteger:
            self.write_production("<Term> -> <Factor> <Term Prime>")
            fact_type = self.factor()
            self.term_prime(fact_type)
            return fact_type
        else:
            self.notify_error("Error: Expected a factor", self.token)
            raise Exception()

    # <Term Prime>
    # This rule comes from fixing the direct left recursion of <Term>
    def term_prime(self, prev_fact_type):
        tok = self.token
        if self.token.value == "*":
            self.write_production("<Term Prime> -> * <Factor> <Term Prime>")
            self.lexer()
            fact_type = self.factor()
            self.gen_instr(MUL, "nil")
            self.term_prime(fact_type)

            # Type check multiplication
            if fact_type == BOOLEAN_T or prev_fact_type == BOOLEAN_T:
                self.notify_error("Error: Cannot multiply booleans", tok)

            return fact_type
        elif self.token.value == "/":
            self.write_production("<Term Prime> -> / <Factor> <Term Prime>")
            self.lexer()
            fact_type = self.factor()
            self.gen_instr(DIV, "nil")
            self.term_prime(fact_type)

            # Type check division
            if fact_type == BOOLEAN_T or prev_fact_type == BOOLEAN_T:
                self.notify_error("Error: Cannot divide booleans", tok)

            return fact_type
        else:
            self.write_production("<Term Prime> -> epsilon")
            return NONE_T

    # <Factor>
    def factor(self):
        tok = self.token
        if self.token.value == "-":
            self.write_production("<Factor> -> - <Primary>")
            self.lexer()
            primary_type = self.primary()

            # Type check negative one coefficient
            if primary_type == BOOLEAN_T:
                self.notify_error("Error: Booleans cannot be negative", tok)

            # Primary will be on top of stack. Push a -1, then MUL to apply the negative
            self.gen_instr(PUSHI, -1)
            self.gen_instr(MUL, "nil")
            return primary_type
        elif self.token.value in {
            "true", "false", "("
            } or self.token.type == TokenIdentifier or self.token.type == TokenInteger:
            self.write_production("<Factor> -> <Primary>")
            return self.primary()
        else:
            self.notify_error("Error: Expected a factor", self.token)
            raise Exception()

    # <Primary>
    def primary(self):
        if self.token.type == TokenIdentifier:
            self.write_production("<Primary> -> <Identifier>")
            addr = self.get_address(self.token.value)
            if addr == -1:
                self.notify_error("Error: Use of undeclared identifier", self.token)
            self.gen_instr(PUSHM, addr)
            tok_id = self.token.value
            self.lexer()
            return INTEGER_T if self.get_type(tok_id) == INTEGER_T else BOOLEAN_T
        elif self.token.type == TokenInteger:
            self.write_production("<Primary> -> <Integer>")
            self.gen_instr(PUSHI, self.token.value)
            self.lexer()
            return INTEGER_T
        elif self.token.value == "(":
            self.write_production("<Primary> -> ( <Expression> )")
            self.lexer()
            expr_type = self.expression()
            if self.token.value == ")":
                self.lexer()
            else:
                self.notify_error("Error: Expected )", self.token)
            return expr_type
        elif self.token.value == "true":
            self.write_production("<Primary> -> true")
            self.gen_instr(PUSHI, 1) # 1 represents true in the VM
            self.lexer()
            return BOOLEAN_T
        elif self.token.value == "false":
            self.write_production("<Primary> -> false")
            self.gen_instr(PUSHI, 0) # 0 represents false in the VM
            self.lexer()
            return BOOLEAN_T
        else:
            self.notify_error("Error: Invalid primary", self.token)
            raise Exception()