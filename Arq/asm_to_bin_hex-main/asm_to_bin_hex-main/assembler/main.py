# ---------------------------
# Main
# ---------------------------

import sys
from assembler.lexer import AsmLexer
from assembler.parser import AsmParser
from assembler.passes import pass1, pass2
from assembler.iohelpers import write_hex_bin

def main():
    if len(sys.argv) != 4:
        print("Usage: python assembler.py program.asm program.hex program.bin")
        sys.exit(1)
    asmfile, hexfile, binfile = sys.argv[1:4]
    txt = open(asmfile, 'r').read()
    lexer = AsmLexer()
    parser = AsmParser()
    tokens = list(lexer.tokenize(txt))
    # parse
    try:
        statements = parser.parse(iter(tokens))
    except Exception as e:
        print("Parse failed:", e)
        sys.exit(1)
    # filter out None lines
    statements = [s for s in statements if s is not None]
    try:
        symtab = pass1(statements)
    except Exception as e:
        print("Pass1 error:", e)
        sys.exit(1)
    try:
        machine = pass2(statements, symtab)
    except Exception as e:
        print("Pass2 error:", e)
        sys.exit(1)
    write_hex_bin(machine, hexfile, binfile)
    print(f"Wrote {len(machine)} words to {hexfile} and {binfile}")

if __name__ == '__main__':
    main()
