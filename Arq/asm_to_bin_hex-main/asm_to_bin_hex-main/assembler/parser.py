# ---------------------------
# Parser (produces a list of statements)
# ---------------------------

from sly import Parser
from assembler.lexer import AsmLexer

class AST:
    pass

class Label(AST):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Label({self.name})"

class Directive(AST):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Directive({self.name})"

class Instr(AST):
    def __init__(self, mnemonic, operands):
        self.mnemonic = mnemonic
        self.operands = operands  # list
    def __repr__(self):
        return f"Instr({self.mnemonic} {self.operands})"

class AsmParser(Parser):
    tokens = AsmLexer.tokens

    # grammar
    @_('lines')
    def program(self, p):
        return p.lines

    @_('line')
    def lines(self, p):
        return [p.line]

    @_('lines line')
    def lines(self, p):
        return p.lines + [p.line]

    @_('LABEL')
    def line(self, p):
        return Label(p.LABEL)

    @_('DIRECTIVE')
    def line(self, p):
        return Directive(p.DIRECTIVE)

    @_('MNEMONIC operands')
    def line(self, p):
        return Instr(p.MNEMONIC, p.operands)

    @_('MNEMONIC')
    def line(self, p):
        return Instr(p.MNEMONIC, [])

    # operands variants: comma-separated, parentheses, registers, numbers, idents
    @_('operand')
    def operands(self, p):
        return [p.operand]

    @_('operands COMMA operand')
    def operands(self, p):
        return p.operands + [p.operand]

    @_('REGISTER')
    def operand(self, p):
        return ('reg', p.REGISTER)

    @_('NUMBER')
    def operand(self, p):
        return ('imm', p.NUMBER)

    @_('MNEMONIC')  # used as identifier operand (label)
    def operand(self, p):
        return ('sym', p.MNEMONIC)

    @_('LPAREN REGISTER RPAREN')
    def operand(self, p):
        # used for offsets like 0(x1)
        return ('paren_reg', p.REGISTER)

    @_('NUMBER LPAREN REGISTER RPAREN')
    def operand(self, p):
        return ('memoff', p.NUMBER, p.REGISTER)

    @_('NEWLINE')
    def line(self, p):
        # blank line -> ignore
        return None

    def error(self, p):
        if p:
            print(f"Parse error near {p.type}({p.value})")
        else:
            print("Parse error at EOF")
        # try to recover by skipping token
        self.errok()
