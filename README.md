# Soft processor
An 8b processor design that can be completly implemented using logic synthesis.
Requirerments: Vivado 2022.2 or newer
This project was made for KV260 Vision AI Starter Kit SOM

### Running project
1) If you have installed Kria Boards installed, then you can run "soft_processor.tcl" in Vivado tcl console, otherwise a new project needs to be created
2) In your open project: Add Sources -> Add or create design sources -> Add directories with Add sources from subdirectories enabled -> Add "soft_processor_Vivado.srcs"

### How to use it
1) Write a program in asembly language in "program.asm" (commands listed below)
2) run "instruction_translator.py" (it will create "program.mc")
3) reload "ins_ROM" ip-core (it will load "program.mc" into ROM)
4) ready to go, u can run a simulation

### Instruction set
\<RX> - Register from 0-7, for example "jump R0"
\<val> - 8b value, can be written in binary (e.g 0b00110011), hexadecimal (e.g. 0xA) or decimal (e.g. 11).
 
- nop - no operation
- jump \<RX> - Jump to the instruction whose address is stored in register \<RX>.
- jumpi \<val> - Jump to the instruction at address \<val>.
- jz \<RX>, \<val> - Jump to instruction \<val> if value in \<RX> is equal to 0.
- jnz \<RX>, \<val> - Jump to instruction \<val> if value in \<RX> is NOT equal to 0.
- movi \<RX>, \<val> - Write \<val> to \<RX>.
- mov \<RX_to>, \<RX_fr> - Copy the value from \<RX_fr> to \<RX_to>.
- add \<RX_to>, \<RX_1>, \<RX_2> - Write sum of values in registers \<RX_1> and \<RX_2> to \<RX_to>.
- addi - \<RX_to>, \<RX_1>, \<val> - Write sum of values in register \<RX_1> and \<val> to \<RX_to>.
- and \<RX_to>, \<RX_1>, \<RX_2> - Bitwise AND operation of values in \<RX_1> and \<RX_2> and write to \<RX_to>.
- andi \<RX_to>, \<RX_1>, \<val> - Bitwise AND operation of values in \<RX_1> and \<val> and write to \<RX_to>.
- load \<RX_to>, \<RX_address> - Load into <RX_to> the value from RAM at the address stored in <RX_address>.
- loadi \<RX_to>, \<val> - Load into <RX_to> the value from RAM at address <val>.

### Architecture
A processor is 8b with 32b instruction set in Harvard architecture with 8 common registers.
 - R0-R3 - General-Purpose Registers,
 - R4 - GPO Register,
 - R5 - GPI Register,
 - R6 - Zero Register,
 - R7 - Instruction Register.
