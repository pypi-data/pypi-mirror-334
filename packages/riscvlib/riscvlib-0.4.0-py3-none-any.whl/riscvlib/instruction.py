import re
from riscvlib.riscvdata import REGISTER_MAP, PSEUDO_INSTRUCTION_MAP, INSTRUCTION_MAP
from riscvlib.utils import sign_extend_str, twos_complement_str


def _get_instruction_type(mnemonic):
    """
    get Instruction Type for a given mnemonic
    :param mnemonic: str - name
    :return: str
    """
    return INSTRUCTION_MAP[mnemonic][4]


def translate_pseudo_instruction(mnemonic, *args):
    """
    Convert a pseudo instruction into one or more standard instructions and apply args
    :param mnemonic: str - the instruction mnemonic
    :param args: list - array of string args
    :return: list - strings; riscv isa instructions
    """
    actual_instructs = PSEUDO_INSTRUCTION_MAP[mnemonic]

    out = []
    # insert args
    for instr_str in actual_instructs:
        for i, arg in enumerate(args):
            # replace placeholder operands in the new instruction with real args
            instr_str = instr_str.replace(f"%arg{i}", arg)
        out.append(instr_str)
    return out


class Instruction:
    """
    Abstract instruction
    """
    mnemonic = None
    opcode = None
    func3 = None
    func7 = None
    _bits = None
    label = None

    def __init__(self, mnemonic: str, *args, label=None, extra_offset=False):
        self.mnemonic = mnemonic
        # look up and set: opcode, func3 and func7 for a given mnemonic
        self.opcode, self.func3, self.func7 = INSTRUCTION_MAP[self.mnemonic][1:4]
        self.args = list(args)
        self.label = label  # label associated with this instruction i.e StartLoop: mv x1, x3
        self.extra_offset = extra_offset  # this was a bonus instruction from a pseudo and adds extra offset ??

    @staticmethod
    def from_line(text: str):
        """
        Create an instruction object from a line of text.
        :param text: string - the instruction i.e add x22, sp, x13
        :return: Instruction
        """
        mnemonic, args = parse_riscv_instruction_line(text)

        if _get_instruction_type(mnemonic) == "R":
            return RInstruction(mnemonic, *args)
        elif _get_instruction_type(mnemonic) == "I":
            return IInstruction(mnemonic, *args)
        elif _get_instruction_type(mnemonic) == "IL":
            return ILInstruction(mnemonic, *args)
        elif _get_instruction_type(mnemonic) == "S":
            return SInstruction(mnemonic, *args)
        elif _get_instruction_type(mnemonic) == "UJ":
            return UJInstruction(mnemonic, *args)
        elif _get_instruction_type(mnemonic) == "U":
            return UInstruction(mnemonic, *args)
        elif _get_instruction_type(mnemonic) == "SB":
            return SBInstruction(mnemonic, *args)
        else:
            raise ValueError(f"Unknown mnemonic '{mnemonic}'")

    def to_bitstring(self):
        """
        Output value as a bitstring
        :return: str - the bit string
        """
        self._build()
        return self._bits

    def to_bytes(self):
        """
        :return: bytes - little endian order
        """
        instr_int = self.to_int()
        return instr_int.to_bytes(4, byteorder='little', signed=False)

    def to_int(self):
        """
        Convert instruction into an integer
        :return: int
        """
        self._build()
        return int(self._bits, 2)

    def _build(self):
        # do all the real work
        raise NotImplementedError("Implement in derived class")

    def __repr__(self):
        return f"{self.__class__.__name__} '{self.mnemonic}' {self.args}"


def parse_riscv_instruction_line(instruction):
    """
    Define a regular expression pattern to match RISC-V instructions
    :param instruction: string - The instruction in the form 'add rd,r1,r2' or 'sw RD, offset(r1)'
    :return: tuple - (mnemonic, *args)
    """
    pattern = r"^\s*([a-zA-Z]+)\s*(.*)$"

    # Match the instruction against the pattern
    match = re.match(pattern, instruction)
    if match:
        mnemonic, operands_str = match.groups()
        operands = [op.strip() for op in operands_str.split(",")]

        # fix for offset style args i.e. 'sw rd, -66(r1)' ignore funct calls
        if len(operands) > 1 and "(" in operands[1] and "%" not in operands[1]:
            r1 = operands[1].split("(")[1].strip(")")
            immd = operands[1].split("(")[0]
            operands = [operands[0], r1, immd]
        return mnemonic, operands
    else:
        raise ValueError(f"Invalid Instruction: '{instruction}'")


def parse_immediate(immediate_str, bits=12, signed=True):
    """
    Parse immediate value, convert to 2's comp and sign extent if necessary
    :param immediate_str: string - dec, hex, octal representation of an immediate value
    :param bits: int - number of bits of output
    :param signed: bool - Output will be treated as signed
    :return: string - the bitstring representing a signed n bit immediate value
    """
    signed_int = 0
    if immediate_str.startswith("0x"):
        # hex
        # convert into binary, will already be 2'complement if negative
        bitstr = bin(int(immediate_str, 16))[2:]  # remove '0x'
        return sign_extend_str(bitstr, bits)
    else:  # chars represent base10 with sign if negative
        # convert the char i.e "-156" to an int -156
        signed_int = int(float(immediate_str))

        if signed_int < 0:
            # neg offsets get 2's comp sign extended
            bit_str = format(signed_int, f'0{bits}b')
            val = twos_complement_str(bit_str)
            return val
        else:
            return f"{signed_int:0{bits}b}"


def parse_address_offset_register(offset_reg_str):
    # i.e.  sw a5,-20(s0)  where -20 is the offset and s0 is reg to offset
    # ret will be offset str and register to offset in a tuple i.e (-20, s0)
    vals = offset_reg_str.split("(")
    vals[1] = vals[1].replace(")", "", 1)
    return f"{parse_immediate(vals[0], bits=12, signed=True)}", vals[1]


class RInstruction(Instruction):
    """
    Regular instruction i.e add x1, x3, x5
    """

    def _build(self):
        rd = REGISTER_MAP[self.args[0]][1]
        rs1 = REGISTER_MAP[self.args[1]][1]
        rs2 = REGISTER_MAP[self.args[2]][1]
        self._bits = f"{self.func7}{rs2:05b}{rs1:05b}{self.func3}{rd:05b}{self.opcode}"

    def __str__(self):
        return f"{self.mnemonic} {self.args[0]}, {self.args[1]}, {self.args[2]}"


class IInstruction(Instruction):
    """
    # immediate type
    "addi",   "slli", "slti", "sltiu", "xori", "slri", "srai", "ori", "andi", "addiw",
    "slliw", "srliw", "sraiw","jalr", "ecall", "ebreak","CSRRW", "CSRRS", "CSRRC",
    "CSRRWI", "CSRRSI", "CSRRCI"
    """
    def _build(self):
        rd = REGISTER_MAP[self.args[0]][1]
        rs1 = REGISTER_MAP[self.args[1]][1]

        immed = str(self.args[2])

        # format immediate as signed binary string
        immd12_signed_bin = parse_immediate(immed)
        self._bits = f"{immd12_signed_bin}{rs1:05b}{self.func3}{rd:05b}{self.opcode}"

    def __str__(self):
        return f"{self.mnemonic} {self.args[0]}, {self.args[1]}, {self.args[2]}"


class ILInstruction(Instruction):
    """
    covers load type IL instructions with the pattern:  inst rd, offset(r1)
    similar to S instruction
    "lb", "lw", "ld", "lbu", "lhu", "lwu",
    """
    def _build(self):
        rd = REGISTER_MAP[self.args[0]][1]  # value to store
        rs1 = REGISTER_MAP[self.args[1]][1]  # holds target address that may be offset

        # offset val for rs1 --> sign extended 12 bits
        offset_val_str = f"{parse_immediate(self.args[2], bits=12, signed=True)}"
        self._bits = f"{offset_val_str}{rs1:05b}{self.func3}{rd:05b}{self.opcode}"

    def __str__(self):
        return f"{self.mnemonic} {self.args[0]}, {self.args[2]}({self.args[1]})"


class SInstruction(Instruction):
    """
    imm[11:5] rs2 rs1 funct3 imm[4:0] opcode     S-type
    i.e. sw rs2,+-offset(rs1)
    The SW, SH, and SB instructions store 32-bit, 16-bit, and 8-bit values from the low
    bits of register rs2 to memory.

    i.e. sw s0,24(sp)
    "sw", "sb", "sh", "sd"
    """

    def _build(self):
        rs2 = REGISTER_MAP[self.args[0]][1]  # value to store
        rs1 = REGISTER_MAP[self.args[1]][1]  # holds target address that may be offset

        # offset val for rs1 --> sign extended 12 bits
        offset_val_str = f"{parse_immediate(self.args[2], bits=12, signed=True)}"

        # split immediate
        imm5 = offset_val_str[7:]
        imm7 = offset_val_str[0:7]

        self._bits = f"{imm7}{rs2:05b}{rs1:05b}{self.func3}{imm5}{self.opcode}"

    def __str__(self):
        return f"{self.mnemonic} {self.args[0]}, {self.args[2]}({self.args[1]})"


class UInstruction(Instruction):
    """
    i.e. LUI x2, 0xfffff000
    """

    def _build(self):
        rd = REGISTER_MAP[self.args[0]][1]

        # check for and get function  ##
        immed = self.args[1]

        # eval expressions if any for the immediate, vars & const have been eval by now
        # so this should be int,bin, hex
        immed = str(immed)
        immd20_bin = parse_immediate(immed, bits=20, signed=False)
        self._bits = f"{immd20_bin}{rd:05b}{self.opcode}"

    def __str__(self):
        return f"{self.mnemonic} {self.args[0]}, {self.args[1]}"


class UJInstruction(Instruction):
    """
     21-bit value in the range of [−1048576..1048574] [-0x100000..0x0ffffe]1561
     representing a pc-relative offset to the target address
     jal x0, -8
    """

    def _build(self):
        rd = REGISTER_MAP[self.args[0]][1]

        # get the bit pattern in the wrong order
        imm_raw = parse_immediate(self.args[1], bits=21, signed=True)

        imm_21_signed = imm_raw[::-1]  # reverse for sanity

        out_sign = imm_21_signed[-1]  # sign
        out_12_19 = imm_21_signed[12:20]  # LSBs
        out_11 = imm_21_signed[11]
        out_1_10 = imm_21_signed[1:11]  # ignore lsb because always even

        out_bits = f"{out_12_19}{out_11}{out_1_10}{out_sign}"[::-1]
        self._bits = f"{out_bits}{rd:05b}{self.opcode}"

    def __str__(self):
        # the UJ type has a varying number of args based on mnemonic
        if self.mnemonic == "jal":
            return f"{self.mnemonic} {self.args[0]}, {self.args[1]}"
        elif self.mnemonic == "jalr":
            return f"{self.mnemonic} {self.args[0]}, {self.args[1]}({self.args[2]})"


class SBInstruction(Instruction):
    """
    Branching instructions
    i.e. beq x3, x0, 33
    beq rs1, rs2, imm
    """

    def _build(self):
        # imm7 rs2 rs1 func3 imm5 opcode
        rs1 = REGISTER_MAP[self.args[0]][1]
        rs2 = REGISTER_MAP[self.args[1]][1]
        
        immd12_signed_bin = parse_immediate(self.args[2], bits=12)
        imb_i12 = immd12_signed_bin[0]  # sign bit
        imb_i11 = immd12_signed_bin[0]  # sign bit... again
        imb_4 = immd12_signed_bin[7:11]  # 4 lsb left right shift 1 fill, because only multiples of 2
        imb_6 = immd12_signed_bin[1:7]  # 6 msb are as they should be
        self._bits = f"{imb_i12}{imb_6}{rs2:05b}{rs1:05b}{self.func3}{imb_4}{imb_i11}{self.opcode}"

    def __str__(self):
        return f"{self.mnemonic} {self.args[0]}, {self.args[1]}, {self.args[2]}"
