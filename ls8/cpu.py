"""CPU functionality."""

import sys

#step 0 inventory files
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #consructor step 1
        #pass
        self.reg = [0]*8
        self.reg[7] = 0xF4
        self.pc = 0
        self.ram = [None] * 256


        #command Translations
        self.SAVE = 0b10000010
        self.PRINT_REG = 0b01000111
        self.HALT = 0b00000001
        self.MULT = 0b10100010
        self.PUSH = 0b010000101
        self.POP = 0b01000110

    #step 2
    def ram_read(self, address):
        return bin(self.ram[address])

    #step 2
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """
        Load a program into memory.
        """
    
        address = 0

   
        program = [
            #From print8.ls8
            #self.SAVE, #LDI RO,8
            0b10000010, #LDI RO, 8
            0b00000000,
            0b00001000,
            0b01000111, #PRN RO
            #0b00010000, 16
            #self.PRINT_REG, #PRN RO
            0b00000000,
            #self.HALT, #HLT
            0b00000001, #HLT
        ]    
        # For now, we've just hardcoded a program:
        '''
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
        '''

        for instruction in program:
            self.ram[address] = instruction
            address += 1
    
    def load_from_file(self):
        file_name = sys.argv[1]
        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()

                    if command == '':
                        continue
                    instruction = int(command, 2)
                    self.ram[address] = instruction

                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

        if len(sys.argv) < 2:
            print('Please pass in a second filename: python3 in_and_out.py second_filename.py')
            sys.exit()
    


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

#step 3
    def run(self):
        """Run the CPU."""
        #pass

        self.pc = 0
        running = True 
        while running:
            command = self.ram[self.pc]

            #Save
            if command == self.SAVE:
                reg = self.ram[self.pc + 1]
                num_to_save = self.ram[self.pc + 2]
                self.reg[reg] = num_to_save
                self.pc += (command >> 6)

            #PRINT_REG
            if command == self.PRINT_REG:
                reg_index = self.ram[self.pc + 1]
                print(self.reg[reg_index])
                self.pc += (command >> 6)

            #MULT
            if command == self.MULT:
                first_reg = self.ram[self.pc + 1]
                sec_reg = self.ram[self.pc + 2]
                self.re[first_reg] = self.reg[first_reg] * self.reg[sec_reg]
                self.pc += (command >> 6)

            #PUSH
            if command == self.PUSH:
                #decrement the stack pointer
                self.reg[7] -= 1

                #get the register number
                reg = self.ram[self.pc + 1]

                #get a value from the given register
                value = self.reg[reg]

                #put the value at the stack pointer address
                sp = self.reg[7]
                self.ram[sp] = value

                #Increment PC
                self.pc += (command >> 6)
            
            #POP
            if command == self.POP:
                #get the stack pointer (where do we look?)
                sp = self.reg[7]

                #get register number to put value in
                reg = self.ram[self.pc + 1]

                #use stack pointer toget the value 
                value = self.ram[sp]

                #put the value into the given register
                self.reg[reg]  = value

                #increment our stack pointer
                self.reg[7] += 1

                #increment our program counter
                self.pc += (command >> 6)
            
            #?step 4
            #HALT
            if command == self.HALT:
                running = False

            self.pc += 1

            #add the HLT
            #add the LDI
            #add the PRN


if __name__ == "__main__":
    cpu = CPU()
    cpu.load_from_file()
    cpu.run()
            

