# ---------------------------
# Instruction table (subset). Extend as needed.
# Each mnemonic mapped to a lambda that takes operands and context and returns 32-bit word
# Context contains: pc, symtab, expand_pseudo -> may be used
# ---------------------------

from assembler.encode import *

OPCODES = {
    # opcode constants
    'LOAD': 0b0000011,
    'STORE':0b0100011,
    'OP_IMM':0b0010011,
    'OP':0b0110011,
    'BRANCH':0b1100011,
    'JALR':0b1100111,
    'JAL':0b1101111,
    'LUI':0b0110111,
    'AUIPC':0b0010111,
    'SYSTEM':0b1110011
}

FUNCTS = {
    # (funct7, funct3) where needed
    'add': (0b0000000, 0b000),
    'sub': (0b0100000, 0b000),
    'sll': (0b0000000, 0b001),
    'slt': (0b0000000, 0b010),
    'sltu':(0b0000000, 0b011),
    'xor': (0b0000000, 0b100),
    'srl': (0b0000000, 0b101),
    'sra': (0b0100000, 0b101),
    'or':  (0b0000000, 0b110),
    'and': (0b0000000, 0b111),
}

# assembler context helpers
class AsmContext:
    def __init__(self, symtab, pc):
        self.symtab = symtab
        self.pc = pc

# helper to resolve immediate or symbol
def resolve_imm_or_sym(op, ctx):
    typ = op[0]
    if typ == 'imm':
        return op[1]
    elif typ == 'sym':
        sym = op[1]
        if sym not in ctx.symtab:
            raise Exception(f"Undefined label: {sym}")
        return ctx.symtab[sym] - ctx.pc
    else:
        raise Exception(f"Expected immediate/label but got {op}")

# encoding functions for common mnemonics (subset)
def assemble_add(operands, ctx):
    # add rd, rs1, rs2
    rd = operands[0][1]
    rs1 = operands[1][1]
    rs2 = operands[2][1]
    funct7, funct3 = FUNCTS['add']
    return encode_r(funct7, rs2, rs1, funct3, rd, OPCODES['OP'])

def assemble_sub(operands, ctx):
    rd = operands[0][1]
    rs1 = operands[1][1]
    rs2 = operands[2][1]
    funct7, funct3 = FUNCTS['sub']
    return encode_r(funct7, rs2, rs1, funct3, rd, OPCODES['OP'])

def assemble_addi(operands, ctx):
    rd = operands[0][1]
    rs1 = operands[1][1]
    imm = operands[2][1]
    # check range -2048..2047
    if imm < -2048 or imm > 2047:
        raise Exception(f"Immediate out of range for addi: {imm}")
    return encode_i(imm & 0xfff, rs1, 0b000, rd, OPCODES['OP_IMM'])

def assemble_lui(operands, ctx):
    rd = operands[0][1]
    imm = operands[1][1]
    # LUI takes upper 20 bits: imm << 12 typically passed as immediate
    return encode_u(imm, rd, OPCODES['LUI'])

def assemble_auipc(operands, ctx):
    rd = operands[0][1]
    imm = operands[1][1]
    return encode_u(imm, rd, OPCODES['AUIPC'])

def assemble_jal(operands, ctx):
    # jal rd, label_or_imm
    rd = operands[0][1]
    target = operands[1]
    if target[0] == 'sym':
        if target[1] not in ctx.symtab:
            raise Exception(f"Undefined label: {target[1]}")
        imm = ctx.symtab[target[1]] - ctx.pc
    elif target[0] == 'imm':
        imm = target[1]
    else:
        raise Exception("Invalid jal operand")
    # imm must be multiple of 1? JAL offset in bytes, range +/- 1MiB
    return encode_j(imm, rd, OPCODES['JAL'])

def assemble_beq(operands, ctx):
    rs1 = operands[0][1]
    rs2 = operands[1][1]
    target = operands[2]
    if target[0] == 'sym':
        if target[1] not in ctx.symtab:
            raise Exception(f"Undefined label: {target[1]}")
        imm = ctx.symtab[target[1]] - ctx.pc
    elif target[0] == 'imm':
        imm = target[1]
    else:
        raise Exception("Invalid branch operand")
    return encode_b(imm, rs2, rs1, 0b000, OPCODES['BRANCH'])

def assemble_bne(operands, ctx):
    rs1 = operands[0][1]
    rs2 = operands[1][1]
    target = operands[2]
    if target[0]=='sym':
        if target[1] not in ctx.symtab:
            raise Exception(f"Undefined label: {target[1]}")
        imm = ctx.symtab[target[1]] - ctx.pc
    else:
        imm = target[1]
    return encode_b(imm, rs2, rs1, 0b001, OPCODES['BRANCH'])

def assemble_blt(operands, ctx):
    rs1 = operands[0][1]
    rs2 = operands[1][1]
    target = operands[2]
    if target[0]=='sym':
        if target[1] not in ctx.symtab:
            raise Exception(f"Undefined label: {target[1]}")
        imm = ctx.symtab[target[1]] - ctx.pc
    else:
        imm = target[1]
    return encode_b(imm, rs2, rs1, 0b100, OPCODES['BRANCH'])

def assemble_bge(operands, ctx):
    rs1 = operands[0][1]
    rs2 = operands[1][1]
    target = operands[2]
    if target[0]=='sym':
        if target[1] not in ctx.symtab:
            raise Exception(f"Undefined label: {target[1]}")
        imm = ctx.symtab[target[1]] - ctx.pc
    else:
        imm = target[1]
    return encode_b(imm, rs2, rs1, 0b101, OPCODES['BRANCH'])

def assemble_bne(operands, ctx):
    rs1 = operands[0][1]
    rs2 = operands[1][1]
    target = operands[2]
    if target[0]=='sym':
        if target[1] not in ctx.symtab:
            raise Exception(f"Undefined label: {target[1]}")
        imm = ctx.symtab[target[1]] - ctx.pc
    else:
        imm = target[1]
    return encode_b(imm, rs2, rs1, 0b001, OPCODES['BRANCH'])

def assemble_blt(operands, ctx):
    rs1 = operands[0][1]
    rs2 = operands[1][1]
    target = operands[2]
    if target[0]=='sym':
        if target[1] not in ctx.symtab:
            raise Exception(f"Undefined label: {target[1]}")
        imm = ctx.symtab[target[1]] - ctx.pc
    else:
        imm = target[1]
    return encode_b(imm, rs2, rs1, 0b100, OPCODES['BRANCH'])

def assemble_bge(operands, ctx):
    rs1 = operands[0][1]
    rs2 = operands[1][1]
    target = operands[2]
    if target[0]=='sym':
        if target[1] not in ctx.symtab:
            raise Exception(f"Undefined label: {target[1]}")
        imm = ctx.symtab[target[1]] - ctx.pc
    else:
        imm = target[1]
    return encode_b(imm, rs2, rs1, 0b101, OPCODES['BRANCH'])

def assemble_bltu(operands, ctx):
    rs1 = operands[0][1]
    rs2 = operands[1][1]
    target = operands[2]
    if target[0]=='sym':
        if target[1] not in ctx.symtab:
            raise Exception(f"Undefined label: {target[1]}")
        imm = ctx.symtab[target[1]] - ctx.pc
    else:
        imm = target[1]
    return encode_b(imm, rs2, rs1, 0b110, OPCODES['BRANCH'])

def assemble_bgeu(operands, ctx):
    rs1 = operands[0][1]
    rs2 = operands[1][1]
    target = operands[2]
    if target[0]=='sym':
        if target[1] not in ctx.symtab:
            raise Exception(f"Undefined label: {target[1]}")
        imm = ctx.symtab[target[1]] - ctx.pc
    else:
        imm = target[1]
    return encode_b(imm, rs2, rs1, 0b111, OPCODES['BRANCH'])

def assemble_lb(operands, ctx):
    rd = operands[0][1]
    # mem operands like imm(reg)
    if operands[1][0] == 'memoff':
        imm = operands[1][1]
        rs1 = operands[1][2]
    else:
        raise Exception("Invalid lb operand")
    return encode_i(imm & 0xfff, rs1, 0b000, rd, OPCODES['LOAD'])

def assemble_sb(operands, ctx):
    # sb rs2, offset(rs1)
    if operands[0][0] != 'reg' or operands[1][0] != 'memoff':
        raise Exception("Invalid sb operand")
    rs2 = operands[0][1]
    imm = operands[1][1]
    rs1 = operands[1][2]
    return encode_s(imm, rs2, rs1, 0b000, OPCODES['STORE'])

def assemble_jalr(operands, ctx):
    # jalr rd, rs1, imm
    rd = operands[0][1]
    rs1 = operands[1][1]
    imm = operands[2][1]
    if imm < -2048 or imm > 2047:
        raise Exception(f"Immediate out of range for jalr: {imm}")
    return encode_i(imm & 0xfff, rs1, 0b000, rd, OPCODES['JALR'])

def assemble_xori(operands, ctx):
    rd = operands[0][1]
    rs1 = operands[1][1]
    imm = operands[2][1]
    if imm < -2048 or imm > 2047:
        raise Exception(f"Immediate out of range for xori: {imm}")
    return encode_i(imm & 0xfff, rs1, 0b100, rd, OPCODES['OP_IMM'])

def assemble_sltiu(operands, ctx):
    rd = operands[0][1]
    rs1 = operands[1][1]
    imm = operands[2][1]
    return encode_i(imm & 0xfff, rs1, 0b011, rd, OPCODES['OP_IMM'])

def assemble_sltu(operands, ctx):
    rd = operands[0][1]
    rs1 = operands[1][1]
    rs2 = operands[2][1]
    funct7, funct3 = FUNCTS['sltu']
    return encode_r(funct7, rs2, rs1, funct3, rd, OPCODES['OP'])

def assemble_slt(operands, ctx):
    rd = operands[0][1]
    rs1 = operands[1][1]
    rs2 = operands[2][1]
    funct7, funct3 = FUNCTS['slt']
    return encode_r(funct7, rs2, rs1, funct3, rd, OPCODES['OP'])

# map mnemonics to assembler functions or to pseudo-expansion
INSTR_TABLE = {
    'add': assemble_add,
    'sub': assemble_sub,
    'addi': assemble_addi,
    'lui': assemble_lui,
    'auipc': assemble_auipc,
    'jal': assemble_jal,
    'beq': assemble_beq,
    'bne': assemble_bne,
    'blt': assemble_blt,
    'bge': assemble_bge,
    'bne': assemble_bne,
    'blt': assemble_blt,
    'bge': assemble_bge,
    'bltu': assemble_bltu,
    'bgeu': assemble_bgeu,
    'lb': assemble_lb,
    'sb': assemble_sb,
    'jalr': assemble_jalr,
    'xori': assemble_xori,
    'sltiu': assemble_sltiu,
    'sltu': assemble_sltu,
    'slt': assemble_slt,
}