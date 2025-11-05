# ---------------------------
# Assembler main logic: two passes
# ---------------------------

from assembler.parser import Directive, Label, Instr
from assembler.pseudo import expand_pseudo
from assembler.instructions import AsmContext, INSTR_TABLE

def pass1(statements):
    symtab = {}
    pc = 0
    in_text = False
    for st in statements:
        if st is None:
            continue
        if isinstance(st, Directive):
            if st.name == '.text':
                in_text = True
                pc = 0  # start text at 0x0
            elif st.name == '.data':
                in_text = False
                # Not implemented: data handling
            continue
        if isinstance(st, Label):
            if st.name in symtab:
                raise Exception(f"Label redefined: {st.name}")
            symtab[st.name] = pc
            continue
        if isinstance(st, Instr):
            # expand pseudoinstr to count instructions
            ex = expand_pseudo(st)
            # every resulting instruction increments pc by 4
            pc += 4 * len(ex)
    return symtab

def pass2(statements, symtab):
    pc = 0
    in_text = False
    machine = []  # list of (address, word)
    for st in statements:
        if st is None:
            continue
        if isinstance(st, Directive):
            if st.name == '.text':
                in_text = True
                pc = 0
            elif st.name == '.data':
                in_text = False
            continue
        if isinstance(st, Label):
            continue
        if isinstance(st, Instr):
            expanded = expand_pseudo(st)
            for einstr in expanded:
                ctx = AsmContext(symtab, pc)
                mnem = einstr.mnemonic
                if mnem in INSTR_TABLE:
                    try:
                        word = INSTR_TABLE[mnem](einstr.operands, ctx)
                    except Exception as e:
                        raise Exception(f"Error assembling {mnem} at 0x{pc:08x}: {e}")
                else:
                    raise Exception(f"Unsupported mnemonic: {mnem}")
                machine.append((pc, word))
                pc += 4
    return machine