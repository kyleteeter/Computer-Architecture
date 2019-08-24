"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 25
        self.reg = [0] * 8
        self.pc = 0
        self.halt = False

        self.ins = {
            ADD: self.op_add,
            HLT: self.op_hlt
        }

    def op_add(self, reg1, reg2):
        self.reg[reg1] += self.reg[reg2]

    def op_hlt(self):
        self.halt = True
        
    def ram_read(self, pc_address):
        return self.ram[pc_address]

    def ram_write(self, value, pc_address):
        self.ram[pc_address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HTL = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010

        running = True
        while running:
            command = self.ram[self.pc]
            if command == HTL:
                running = False
            elif command == LDI:
                #reg location
                operand_a = self.ram_read(self.pc + 1)
                #value
                operand_b = self.ram_read(self.pc + 2)
                #set value of a register to an integer
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif command == PRN:
                #Print numeric value stored in the given register
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2
            else:
                print("Error: Command not found")

