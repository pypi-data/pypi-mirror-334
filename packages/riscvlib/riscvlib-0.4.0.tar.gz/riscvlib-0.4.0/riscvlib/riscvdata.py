

#  instruction: (name, opcode, func3, func7, itype, ext)
INSTRUCTION_MAP = {
    'add': ('ADD', '0110011', '000', '0000000', 'R', 'i'),
    'sub': ('SUB', '0110011', '000', '0100000', 'R', 'i'),
    'sll': ('SLL', '0110011', '001', '0000000', 'R', 'i'),
    'slt': ('SLT', '0110011', '010', '0000000', 'R', 'i'),
    'sltu': ('SLTU', '0110011', '011', '0000000', 'R', 'i'),
    'xor': ('XOR', '0110011', '100', '0000000', 'R', 'i'),
    'srl': ('SRL', '0110011', '101', '0000000', 'R', 'i'),
    'sra': ('SRA', '0110011', '101', '0100000', 'R', 'i'),
    'or': ('OR', '0110011', '110', '0000000', 'R', 'i'),
    'and': ('AND', '0110011', '111', '0000000', 'R', 'i'),
    'addw': ('ADDW', '0111011', '000', '0000000', 'R', 'i'),
    'subw': ('SUBW', '0111011', '000', '0100000', 'R', 'i'),
    'sllw': ('SLLW', '0111011', '001', '0000000', 'R', 'i'),
    'slrw': ('SLRW', '0111011', '101', '0000000', 'R', 'i'),
    'sraw': ('SRAW', '0111011', '101', '0100000', 'R', 'i'),
    'addi': ('ADDI', '0010011', '000', None, 'I', 'i'),
    'lb': ('LB', '0000011', '000', None, 'IL', 'i'),
    'lh': ('LH', '0000011', '001', None, 'IL', 'i'),
    'lw': ('LW', '0000011', '010', None, 'IL', 'i'),
    'ld': ('LD', '0000011', '011', None, 'IL', 'i'),
    'lbu': ('LBU', '0000011', '100', None, 'IL', 'i'),
    'lhu': ('LHU', '0000011', '101', None, 'IL', 'i'),
    'lwu': ('LWU', '0000011', '110', None, 'IL', 'i'),
    'fence': ('FENCE', '0001111', '000', None, 'I', 'i'),
    'fence.i': ('FENCE.I', '0001111', '001', None, 'I', 'i'),
    'slli': ('SLLI', '0010011', '001', '0000000', 'I', 'i'),
    'slti': ('SLTI', '0010011', '010', None, 'I', 'i'),
    'sltiu': ('SLTIU', '0010011', '011', None, 'I', 'i'),
    'xori': ('XORI', '0010011', '100', None, 'I', 'i'),
    'slri': ('SLRI', '0010011', '101', '0000000', 'I', 'i'),
    'srai': ('SRAI', '0010011', '101', '0100000', 'I', 'i'),
    'ori': ('ORI', '0010011', '110', None, 'I', 'i'),
    'andi': ('ANDI', '0010011', '111', None, 'I', 'i'),
    'addiw': ('ADDIW', '0011011', '000', None, 'I', 'i'),
    'slliw': ('SLLIW', '0011011', '001', '0000000', 'I', 'i'),
    'srliw': ('SRLIW', '0011011', '101', '0000000', 'I', 'i'),
    'sraiw': ('SRAIW', '0011011', '101', '0100000', 'I', 'i'),
    'jalr': ('JALR', '1100111', '000', None, 'I', 'i'),
    'ecall': ('ECALL', '1110011', '000', '000000000000', 'I', 'i'),
    'ebreak': ('EBREAK', '1110011', '000', '000000000001', 'I', 'i'),
    'csrrw': ('CSRRW', '1110011', '001', None, 'I', 'i'),
    'csrrs': ('CSRRS', '1110011', '010', None, 'I', 'i'),
    'csrrc': ('CSRRC', '1110011', '011', None, 'I', 'i'),
    'csrrwi': ('CSRRWI', '1110011', '101', None, 'I', 'i'),
    'csrrsi': ('CSRRSI', '1110011', '110', None, 'I', 'i'),
    'csrrci': ('CSRRCI', '1110011', '111', None, 'I', 'i'),
    'sw': ('SW', '0100011', '010', None, 'S', 'i'),
    'sb': ('SB', '0100011', '000', None, 'S', 'i'),
    'sh': ('SH', '0100011', '001', None, 'S', 'i'),
    'sd': ('SD', '0100011', '011', None, 'S', 'i'),
    'beq': ('BEQ', '1100011', '000', None, 'SB', 'i'),
    'bne': ('BNE', '1100011', '001', None, 'SB', 'i'),
    'blt': ('BLT', '1100011', '100', None, 'SB', 'i'),
    'bge': ('BGE', '1100011', '101', None, 'SB', 'i'),
    'bltu': ('BLTU', '1100011', '110', None, 'SB', 'i'),
    'bgeu': ('BGEU', '1100011', '111', None, 'SB', 'i'),
    'auipc': ('AUIPC', '0010111', None, None, 'U', 'i'),
    'lui': ('LUI', '0110111', None, None, 'U', 'i'),
    'jal': ('JAL', '1101111', None, None, 'UJ', 'i'),
    'mul': ('MUL', '0110011', '000', '0000001', 'R', 'm'),
    'mulh': ('MULH', '0110011', '001', '0000001', 'R', 'm'),
    'mulhsu': ('MULHSU', '0110011', '010', '0000001', 'R', 'm'),
    'mulhu': ('MULHU', '0110011', '011', '0000001', 'R', 'm'),
    'div': ('DIV', '0110011', '100', '0000001', 'R', 'm'),
    'divu': ('DIVU', '0110011', '101', '0000001', 'R', 'm'),
    'rem': ('REM', '0110011', '110', '0000001', 'R', 'm'),
    'remu': ('REMU', '0110011', '111', '0000001', 'R', 'm')
}

# map pseudo instruction name --> implementation with arg placeholders
PSEUDO_INSTRUCTION_MAP = {
    "mv": ["addi %arg0, %arg1, 0"],  # move
    "nop": ["addi x0, x0, 0"],   # no op
    "not": ["xori %arg0, %arg1, -1"],  # One's complement
    "neg": ["sub %arg0, x0, %arg1"],  # Two's complement
    "seqz": ["sltiu %arg0, %arg1, 1"],  # Set if = zero
    "li": ["addi %arg0, x0, %arg1"],
    "call": ["jal x1, %arg0"],   # invoke subroutines

    # jumps/returns
    "j": ["jal x0, %arg0"],    # Jump
    "jr": ["jalr x0, %arg0, 0"],  # Jump register
    "ret": ["jalr x0, x1, 0"],  # Return from subroutine

    # branching
    "beqz": ["beq %arg0, x0, %arg1"],  # branch eq zero
    "bnez": ["bne %arg0, x0, %arg1"],  # branch not eq zero
    "blez": ["bge x0, %arg0, %arg1"],  # Branch if ≤ zero
    "bgez": ["bge %arg0, x0, %arg1"],  # Branch if ≥ zero
    "bltz": ["blt %arg0, x0, %arg1"],  # Branch if < zero
    "bgtz": ["blt x0, %arg0, %arg1"],  # Branch if > zero
    # Note: args pos change
    "bgt": ["blt %arg1, %arg0, %arg2"],  # Branch if >
    "ble": ["bge %arg1, %arg0, %arg2"],  # Branch if ≤
    "bgtu": ["bltu %arg1, %arg0, %arg2"],  # Branch if >, unsigned
    "bleu": ["bgeu %arg1, %arg0, %arg2"],  # Branch if ≤, unsigned
    # mult instructs returned
    "la": ["lui %arg0, %hi(%arg1)", "addi %arg0, %arg0, %lo(%arg1)"],
}

# list of pseudo instructions
pseudo_instr_list = list(PSEUDO_INSTRUCTION_MAP.keys())


# registers  "lookup": ('name', int)
REGISTER_MAP = {
    'x0': ('x0', 0), 'zero': ('x0', 0), 'x1': ('x1', 1), 'ra': ('x1', 1), 'x2': ('x2', 2), 'sp': ('x2', 2),
    'x3': ('x3', 3), 'gp': ('x3', 3), 'x4': ('x4', 4), 'tp': ('x4', 4), 'x5': ('x5', 5), 't0': ('x5', 5),
    'x6': ('x6', 6), 't1': ('x6', 6), 'x7': ('x7', 7), 't2': ('x7', 7), 'x8': ('x8', 8),
    'x9': ('x9', 9), 's1': ('x9', 9), 'x10': ('x10', 10), 'a0': ('x10', 10), 'x11': ('x11', 11),
    'a1': ('x11', 11), 'x12': ('x12', 12), 'a2': ('x12', 12), 'x13': ('x13', 13), 'a3': ('x13', 13),
    'x14': ('x14', 14), 'a4': ('x14', 14), 'x15': ('x15', 15), 'a5': ('x15', 15), 'x16': ('x16', 16),
    'a6': ('x16', 16), 'x17': ('x17', 17), 'a7': ('x17', 17), 'x18': ('x18', 18), 's2': ('x18', 18),
    'x19': ('x19', 19), 's3': ('x19', 19), 'x20': ('x20', 20), 's4': ('x20', 20), 'x21': ('x21', 21),
    's5': ('x21', 21), 'x22': ('x22', 22), 's6': ('x22', 22), 'x23': ('x23', 23), 's7': ('x23', 23),
    'x24': ('x24', 24), 's8': ('x24', 24), 'x25': ('x25', 25), 's9': ('x25', 25), 'x26': ('x26', 26),
    's10': ('x26', 26), 'x27': ('x27', 27), 's11': ('x27', 27), 'x28': ('x28', 28), 't3': ('x28', 28),
    'x29': ('x29', 29), 't4': ('x29', 29), 'x30': ('x30', 30), 't5': ('x30', 30), 'x31': ('x31', 31),
    't6': ('x31', 31), 's0': ('x8', 8), 'fp': ('x8', 8)
}
