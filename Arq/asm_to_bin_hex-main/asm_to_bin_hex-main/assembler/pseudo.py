# ---------------------------
# pseudoinstructions expansion
# ---------------------------

from assembler.parser import Instr

def expand_pseudo(instr):
    m = instr.mnemonic
    ops = instr.operands
    expanded = []
    if m == 'nop':
        # nop -> addi x0, x0, 0
        expanded.append(Instr('addi', [('reg', 0), ('reg', 0), ('imm', 0)]))
    elif m == 'mv':
        # mv rd, rs -> addi rd, rs, 0
        expanded.append(Instr('addi', [ops[0], ops[1], ('imm',0)]))
    elif m == 'li':
        # li rd, imm -> if imm fits in 12 bits -> addi; else use lui/addi
        rd = ops[0]
        immval = ops[1][1]
        if -2048 <= immval <= 2047:
            expanded.append(Instr('addi', [rd, ('reg',0), ('imm', immval)]))
        else:
            # LO/HI split: simple approach: use lui + addi with immediate lower bits
            hi = (immval + (1<<11)) & ~0xfff
            lo = immval - hi
            expanded.append(Instr('lui', [rd, ('imm', hi)]))
            expanded.append(Instr('addi', [rd, ('reg', rd[1] if rd[0]=='reg' else 0), ('imm', lo)]))
    elif m == 'j':
        # j label -> jal x0, label
        expanded.append(Instr('jal', [ ('reg', 0), ops[0] ]))
    elif m == 'jr':
        # jr rs -> jalr x0, rs, 0
        expanded.append(Instr('jalr', [ ('reg',0), ops[0], ('imm',0) ]))
    elif m == 'ret':
        # ret -> jalr x0, x1, 0
        expanded.append(Instr('jalr', [('reg',0), ('reg',1), ('imm',0)]))
    elif m == 'jalr':  
        # pseudoinstrucción jalr rs -> jalr x1, rs, 0
        if len(ops)==1:
            expanded.append(Instr('jalr', [('reg',1), ops[0], ('imm',0)]))
    elif m == 'beqz':
        # beqz rs, label -> beq rs, x0, label
        expanded.append(Instr('beq', [ops[0], ('reg',0), ops[1]]))
    elif m == 'bnez':
        expanded.append(Instr('bne', [ops[0], ('reg',0), ops[1]]))
    elif m == 'bgez':
        expanded.append(Instr('bge', [ops[0], ('reg',0), ops[1]]))
    elif m == 'bltz':
        expanded.append(Instr('blt', [ops[0], ('reg',0), ops[1]]))
    elif m == 'bgtz':
        expanded.append(Instr('blt', [('reg',0), ops[0], ops[1]]))
    elif m == 'la':
        # la rd, symbol -> addi rd, rd, symbol[11:0]
        expanded.append(Instr('addi', [ops[0], ops[0], ('sym', ops[1][1])]))
    elif m in ('lb','lh','lw'):
        # l{b,h,w} rd, symbol -> rd = symbol[11:0](x0)
        expanded.append(Instr(m, [ops[0], ('memoff', 0, 0)]))  # simplificado
    elif m in ('sb','sh','sw'):
        # s{b,h,w} rd, symbol
        expanded.append(Instr(m, [ops[0], ('memoff', 0, 0)]))
    elif m == 'not':
        # not rd, rs -> xori rd, rs, -1
        expanded.append(Instr('xori', [ops[0], ops[1], ('imm', -1)]))
    elif m == 'neg':
        # neg rd, rs -> sub rd, x0, rs
        expanded.append(Instr('sub', [ops[0], ('reg',0), ops[1]]))
    elif m == 'seqz':
        expanded.append(Instr('sltiu', [ops[0], ops[1], ('imm',1)]))
    elif m == 'snez':
        expanded.append(Instr('sltu', [ops[0], ('reg',0), ops[1]]))
    elif m == 'sltz':
        expanded.append(Instr('slt', [ops[0], ops[1], ('reg',0)]))
    elif m == 'sgtz':
        expanded.append(Instr('slt', [ops[0], ('reg',0), ops[1]]))
    # --- branches ---
    elif m == 'beqz':
        expanded.append(Instr('beq', [ops[0], ('reg',0), ops[1]]))
    elif m == 'bnez':
        expanded.append(Instr('bne', [ops[0], ('reg',0), ops[1]]))
    elif m == 'blez':
        expanded.append(Instr('bge', [('reg',0), ops[0], ops[1]]))
    elif m == 'bgez':
        expanded.append(Instr('bge', [ops[0], ('reg',0), ops[1]]))
    elif m == 'bltz':
        expanded.append(Instr('blt', [ops[0], ('reg',0), ops[1]]))
    elif m == 'bgtz':
        expanded.append(Instr('blt', [('reg',0), ops[0], ops[1]]))
    elif m == 'bgt':
        expanded.append(Instr('blt', [ops[1], ops[0], ops[2]]))
    elif m == 'ble':
        expanded.append(Instr('bge', [ops[1], ops[0], ops[2]]))
    elif m == 'bgtu':
        expanded.append(Instr('bltu', [ops[1], ops[0], ops[2]]))
    elif m == 'bleu':
        expanded.append(Instr('bgeu', [ops[1], ops[0], ops[2]]))
    # --- jumps ---
    elif m == 'jal' and len(ops)==1:
        # jal offset -> jal x1, offset
        expanded.append(Instr('jal', [('reg',1), ops[0]]))
    elif m == 'jalr' and len(ops)==1:
        # jalr rs -> jalr x1, rs, 0
        expanded.append(Instr('jalr', [('reg',1), ops[0], ('imm',0)]))
    elif m == 'ret':
        expanded.append(Instr('jalr', [('reg',0), ('reg',1), ('imm',0)]))
    elif m == 'call':
        # call offset -> jalr x1,x1,offset[11:0]
        expanded.append(Instr('jalr', [('reg',1), ('reg',1), ops[0]]))
    elif m == 'tail':
        # tail offset -> jalr x0,x6,offset[11:0]
        expanded.append(Instr('jalr', [('reg',0), ('reg',6), ops[0]]))
    else:
        return [instr]
    return expanded