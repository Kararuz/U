# ---------------------------
# Instruction encoding helpers
# ---------------------------

def sign_extend(x, bits):
    mask = (1 << bits) - 1
    x &= mask
    if x & (1 << (bits - 1)):
        return x - (1 << bits)
    return x

def u32(x):
    return x & 0xFFFFFFFF

def encode_r(funct7, rs2, rs1, funct3, rd, opcode):
    return u32((funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode)

def encode_i(imm, rs1, funct3, rd, opcode):
    imm12 = imm & 0xFFF
    return u32((imm12 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode)

def encode_s(imm, rs2, rs1, funct3, opcode):
    imm12 = imm & 0xFFF
    imm11_5 = (imm12 >> 5) & 0x7F
    imm4_0 = imm12 & 0x1F
    return u32((imm11_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm4_0 << 7) | opcode)

def encode_b(imm, rs2, rs1, funct3, opcode):
    # imm is branch offset in bytes; must be multiple of 2
    imm12 = imm & 0x1FFF  # take enough bits
    # B-type encoding: imm[12] | imm[10:5] | rs2 | rs1 | funct3 | imm[4:1] | imm[11] | opcode
    bit_12 = (imm12 >> 12) & 0x1
    bits_10_5 = (imm12 >> 5) & 0x3F
    bits_4_1 = (imm12 >> 1) & 0xF
    bit_11 = (imm12 >> 11) & 0x1
    instr = (bit_12 << 31) | (bits_10_5 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (bits_4_1 << 8) | (bit_11 << 7) | opcode
    return u32(instr)

def encode_u(imm, rd, opcode):
    # imm is upper 20 bits << 12
    imm20 = imm & 0xFFFFF000
    return u32((imm20) | (rd << 7) | opcode)

def encode_j(imm, rd, opcode):
    # J-type: imm[20] | imm[10:1] | imm[11] | imm[19:12]
    imm20 = imm & 0x1FFFFF
    bit20 = (imm20 >> 20) & 0x1
    bits10_1 = (imm20 >> 1) & 0x3FF
    bit11 = (imm20 >> 11) & 0x1
    bits19_12 = (imm20 >> 12) & 0xFF
    instr = (bit20 << 31) | (bits19_12 << 12) | (bit11 << 20) | (bits10_1 << 21) | (rd << 7) | opcode
    return u32(instr)
