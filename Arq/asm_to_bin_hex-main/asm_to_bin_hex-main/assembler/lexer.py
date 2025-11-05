# ---------------------------
# Lexer
# ---------------------------

from sly import Lexer

class AsmLexer(Lexer):
    # Define los nombres de los tokens en un set de strings
    tokens = {
        'IDENT', 'MNEMONIC', 'REGISTER', 'NUMBER',
        'DIRECTIVE', 'LABEL', 'COMMA', 'LPAREN',
        'RPAREN', 'COLON', 'NEWLINE'
    }

    # Caracteres ignorados y comentarios
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Definición de símbolos simples
    COMMA  = r','
    LPAREN = r'\('
    RPAREN = r'\)'
    COLON  = r':'
    NEWLINE = r'\n+'

    # directives like .text .data
    @_(r'\.[A-Za-z]+')
    def DIRECTIVE(self, t):
        t.value = t.value.lower()
        return t

    # labels: identifier followed by :
    @_(r'[A-Za-z_]\w*:')
    def LABEL(self, t):
        t.value = t.value[:-1]
        return t

    # registers: x0..x31 or aliases (we'll support xN)
    @_(r'x([0-2]?\d|3[01])\b')
    def REGISTER(self, t):
        t.value = int(t.value[1:])
        return t

    # mnemonics: letters and optional dots? treat as IDENT then parser may treat as mnemonic
    @_(r'[A-Za-z][A-Za-z0-9_\.]*')
    def IDENT(self, t):
        # classify mnemonic vs identifier by value later in parser
        # we'll send as MNEMONIC by default
        t.type = 'MNEMONIC'
        t.value = t.value.lower()
        return t

    # numbers: decimal, hex 0x..., binary 0b...
    @_(r'0x[0-9A-Fa-f]+')
    def NUMBER(self, t):
        t.value = int(t.value, 16)
        return t

    @_(r'0b[01]+')
    def NUMBER(self, t):
        t.value = int(t.value, 2)
        return t

    @_(r'-?\d+')
    def NUMBER(self, t):
        t.value = int(t.value, 10)
        return t

    # error
    def error(self, t):
        print(f'Lexer: illegal character {t.value[0]!r} at line {self.lineno}')
        self.index += 1
        