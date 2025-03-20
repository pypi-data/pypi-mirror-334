# riscvlib  
  
Resources for working with RiscV assembly in Python. 
Supporting RV32IM instruction creation, pseudo instruction translation and register lookup.
  
# Installation  
The package can be installed using pip:  
  
	 $ pip install riscvlib  
 
# Examples  
  
## Instruction, Static creation from a string
``` python
>> from riscvlib.instruction import Instruction  

>> i = Instruction.from_line("add x1, x2, x3")  
>> print(i) 
add x1, x2, x3  
>> i.to_bytes() 
b'\xb3\x001\x00'  
>> i  
RInstruction 'add' ['x1', 'x2', 'x3']
```

## Specific Instruction Type
``` python
>> from riscvlib.instruction import RInstruction, IInstruction

>> r_instr = RInstruction("add", "x1", "x2", "a2")
>> print(r_instr)
add x1, x2, a2

>> i_instr = IInstruction("andi", "a0", "a1", -13)
>> print(i_instr)
andi a0, a1, -13
>> i_instr.to_bytes()  # note: bytes are 'little endian' ordered
b'\x13\xf55\xff'
```

## Pseudo Instruction Translation
``` python
>> from riscvlib.instruction import translate_pseudo_instruction

>> out_list = translate_pseudo_instruction("mv", "a0", "x30")
>> print(out_list)
['addi a0, x30, 0']

>> out_list = translate_pseudo_instruction("la", "a0", "400")
>> print(out_list)
['lui a0, %hi(400)', 'addi a0, a0, %lo(400)']
```

## Instruction Data
``` python
>> from riscvlib.risvdata import INSTRUCTION_MAP

>> INSTRUCTION_MAP['mul']
('MUL', '0110011', '000', '0000001', 'R', 'm')
# (name, opcode, func3, func7, itype, extension)
```

# Limitations
 - Currently only supports RV32IM (RiscV 32 bit I and M extensions)

# Future
 - Add B extension
 - Add F extension/register look-ups
 - 64 bit support (far future)



