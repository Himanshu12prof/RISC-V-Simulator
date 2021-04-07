from bitstring import BitArray
import json

def programRun():
    Execute = execute()
    machine_file = open("code.mc", "r")
    machine_code = machine_file.read()
    machine_file.close()
    print(machine_code)
    try:
        if(machine_code!=""):
            Execute.storeInstruction(machine_code)
            Execute.run()
            memory = Execute.Memory.returns()
            data ={}
            for i in memory :
                data[hex(i)] = memory[i]
            with open('memory.mc', 'w') as outfile:
                json.dump(data, outfile, indent=4)
            print("No. of Cycles taken to execute the program : "+str(Execute.cycle))


        else:
            print("Input Valid mc code")
    except:
        print("Input Valid mc code")

class execute :

    # initialinzing the code
    def __init__(self) :
        self.Register = register()  #creating register
        self.Memory = memory()  #creating memory
        self.sp =0x7ffffffc
        self.PC = 0
        self.instruction = 0

    #  storing the instruction in the memory file
    def storeInstruction(self,machine_code):
        self.Register.flush()
        self.Memory.flush()
        self.PC = 0
        self.cycle = 0
        self.Register.update("00010", self.sp)

        if (machine_code == None):
            return "no code provided"
        else :
            # spliting the machine code and storing in the list
            machine_code = machine_code.splitlines()
            for line in machine_code:
                try:
                    address, instruction = line.split()
                    address = int(address,16)
                    value = BitArray(hex = instruction).int
                    self.Memory.writeWord(address,value)
                except:
                    return "some problem in storing the instruction in memory"

    def run(self) :

        print("\n|-----------State before the execution of the program -------------|\n")
        print("Register: ")
        print(self.Register.returns())
        print("Memory: ")
        print(self.Memory.returns())
        print("\n|-----------Execution of the program start-------|\n")
        while self.Memory.readWord(self.PC) != 0:
            self.fetch()
        print("\n-------After Execution of the program -------\n")
        print("Register: ")
        print(self.Register.returns())
        print("Memory: ")
        print(self.Memory.returns())

    def fetch(self):
        print("\n|------------Fetching of the instruction---------------|\n")
        self.cycle += 1
        #Fetching next instruction to process
        self.instruction = self.Memory.readWord(self.PC)
        self.instruction = BitArray(int = self.instruction, length = 32).bin
        print("instruction:"+str(self.instruction))

        #Increase PC for next instruction
        self.PC = self.PC + 4

        #now going to the next step of execution
        self.decode()

    def checkFormat(self):

        # storing the part of the opcode of every insstruction
        i_OR_s = ["0000011", "0001111", "0010011", "0011011", "0100011", "1100111", "1110011"]
        r = ["0110011", "0111011"]
        u = ["0010111", "0110111"]
        sb = "1100011"
        uj = "1101111"

        # checking the type
        if self.opcode in r:
            return "r"
        elif self.opcode in u:
            return "u"
        elif self.opcode == sb:
            return "sb"
        elif self.opcode == uj:
            return "uj"
        elif self.opcode in i_OR_s:
            if self.opcode == "0100011" and self.funct3 != "011":
                return "s"
            else:
                return "i"
        else :
            print("no Format match")
            return "none"

    def decode(self):
        print("\n|--------------Decode of the instruction-------------|\n")

        # extracting the opcode
        self.opcode = self.instruction[25:32]
        print("opcode:"+self.opcode)

        # checking the format of the instruction
        format = self.checkFormat()
        print("format:"+format)

        # assigning all the control signals
        self.memory_enable = False
        self.write_enable = True
        self.muxY = 0
        self.RZ = 0

        if format == "r":
            self.decodeR()
        elif format == "i":
            self.decodeI()
        elif format == "s":
            self.decodeS()
        elif format == "sb":
            self.decodeSB()
        elif format == "u":
            self.decodeU()
        elif format == "uj":
            self.decodeUJ()

    def decodeR(self):

        # Extracting the part of the instruction
        self.RS1 = self.instruction[12:17]
        print("RS1:" + self.RS1)
        self.RS2 = self.instruction[7:12]
        print("RS2:" + self.RS2)
        self.RD = self.instruction[20:25]
        print("RD:" + self.RD)
        self.RA = self.Register.read(self.RS1)  # Loading value of register at rs1
        print("RA:" + str(self.RA))
        self.RB = self.Register.read(self.RS2)  # Loading value of register at rs2
        print("RB:" + str(self.RB))
        self.funct3 = self.instruction[17:20]
        self.funct7 = self.instruction[0:7]

        # assigning the values of the control signal
        self.muxB = 0
        self.muxY = 0

        # assigning the instruction to the ALU
        if self.funct3 == "000":
            if self.funct7 == "0000000":
                self.alu("add")  # add
            elif self.funct7 == "0000001":
                self.alu("mul")  # mul
            elif self.funct7 == "0100000":
                self.alu("sub")  # sub
        elif self.funct3 == "110":
            if self.funct7 == "0000000":
                self.alu("or")  # or
            elif self.funct7 == "0000001":
                self.alu("rem")  # rem
        elif self.funct3 == "100":
            if self.funct7 == "0000000":
                self.alu("xor")  # xor
            elif self.funct7 == "0000001":
                self.alu("div")  # div
        elif self.funct3 == "101":
            if self.funct7 == "0000000":
                self.alu("srl")  # srl
            elif self.funct7 == "0100000":
                self.alu("sra")  # sra
        elif self.funct3 == "111" and self.funct7 == "0000000":
            self.alu("and")  # and
        elif self.funct3 == "001" and self.funct7 == "0000000":
            self.alu("sll")  # sll
        elif self.funct3 == "010" and self.funct7 == "0000000":
            self.alu("slt")  # slt
        else :
            print("No match found in the R format")

    def decodeI(self):

        # extracting all the feilds of the instruction
        self.RS1 = self.instruction[12:17]
        print("RS1:"+self.RS1)
        self.RA = self.Register.read(self.RS1)
        print("RA:"+str(self.RA))
        self.funct3 = self.instruction[17:20]
        print("funct3:"+self.funct3)
        self.imm = BitArray(bin = self.instruction[0:12]).int
        print("imm:"+str(self.imm))
        self.RD = self.instruction[20:25]
        print("RD:"+self.RD)
        self.muxB = 1

        # assigning the instruction to the ALU

        if self.opcode == "0010011" and self.funct3 == "000":
            self.muxY = 0
            self.alu("add")                 #addi
        elif self.opcode == "1100111" and self.funct3 == "000":
            self.muxY = 2
            self.alu("jalr")                #jalr
        elif self.opcode == "0010011":
            if self.funct3 == "110":
                self.muxY = 0
                self.alu("or")             #ori
            elif self.funct3 == "111":
                self.muxY = 0
                self.alu("and")             #andi
        elif self.opcode == "0000011" and (self.funct3 == "010" or self.funct3 == "000" or self.funct3 == "001" or self.funct3 == "100" or self.funct3 == "101"):
            self.muxY = 1
            self.memory_enable = True
            self.alu("add")    #all load ins lb, lh, lw
        else :
            print("No match found in I format")

    def decodeS(self):
        # extracting all the feilds of the instruction
        self.RS1 = self.instruction[12:17]
        print("RS1:"+self.RS1)
        self.RA = self.Register.read(self.RS1)
        print("RA:"+str(self.RA))
        self.funct3 = self.instruction[17:20]
        print("funct3:"+self.funct3)
        self.RS2 = self.instruction[7:12]
        print("RS2:"+self.RS2)
        self.RB = self.Register.read(self.RS2)
        print("RB:"+str(self.RB))
        imm1 = self.instruction[0:7]
        imm2 = self.instruction[20:25]
        self.write_enable = False
        self.imm = BitArray(bin = imm1+imm2).int

        # assigning the instruction to the ALU
        if self.funct3 == "010" or self.funct3 == "000" or self.funct3 == "001":
            self.RM = self.RB
            self.muxB = 1
            self.memory_enable = True
            self.alu("add")                 #sw or sb or sh
        else :
            print("No match found in S format")

    def decodeSB(self):

        # Exxtracting the part of the instruction
        self.RS1 = self.instruction[12:17]
        print("RS1:"+self.RS1)
        self.RS2 = self.instruction[7:12]
        print("RS2:"+self.RS2)
        self.RA = self.Register.read(self.RS1)
        print("RA:"+str(self.RA))
        self.RB = self.Register.read(self.RS2)
        print("RB:"+str(self.RB))
        self.funct3 = self.instruction[17:20]
        imm1 = self.instruction[0]
        imm2 = self.instruction[24]
        imm3 = self.instruction[1:7]
        imm4 = self.instruction[20:24]
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int

        # assgining the value of the control signal
        self.muxB = 0
        self.write_enable = False

        # assigning the instruction to the ALU
        if self.funct3 == "000":
            print("going to beq")
            self.alu("beq")                 #beq
        elif self.funct3 == "101":
            self.alu("bge")                 #bge
        elif self.funct3 == "100":
            self.alu("blt")                 #blt
        elif self.funct3 == "001":
            self.alu("bne")                 #bne
        else :
            print("No match found in SB format")

    def decodeU(self):

        # extracting all the part of the instruction
        self.RD = self.instruction[20:25]
        print("RD:"+self.RD)
        imm1 = self.instruction[0:20]
        imm2 = "000000000000"
        self.imm = BitArray(bin = imm1 + imm2).int

        # assigning the instruction to the ALU
        if self.opcode == "0110111":
            self.RA = 0
            self.muxB = 1
            self.alu("add")                 #lui
        else:
            self.alu("auipc")               #auipc

    def decodeUJ(self):
        self.RD = self.instruction[20:25]
        print("RD:"+self.RD)
        imm1 = self.instruction[0]
        imm2 = self.instruction[12:20]
        imm3 = self.instruction[11]
        imm4 = self.instruction[1:11]
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int
        self.muxY = 2
        self.alu("jal")                     #jal

    def alu(self,operation):
        print("\n|--------- (ALU Part)Execution of the instruction----------|\n")
        print("OP:",operation)
        if operation == "add":
            if self.muxB == 0:
                self.RZ = self.RA + self.RB   #add
            if self.muxB == 1:
                self.RZ = self.RA + self.imm  #addi
        elif operation == "mul":
            self.RZ = self.RA * self.RB
        elif operation == "sub":
            self.RZ = self.RA - self.RB
        elif operation == "or":
            if self.muxB == 0:
                self.RZ = self.RA | self.RB   #or
            elif self.muxB == 1:
                self.RZ = self.RA | self.imm  #ori
        elif operation == "rem":
            self.RZ = self.RA % self.RB
        elif operation == "xor":
            self.RZ = self.RA ^ self.RB
        elif operation == "div":
            self.RZ = self.RA // self.RB
        elif operation == "srl":
            self.RZ = BitArray(int=self.RA, length=32) >> self.RB
            self.RZ = self.RZ.int
        elif operation == "sra":
            self.RZ = self.RA >> self.RB
        elif operation == "and":
            if self.muxB == 0:
                self.RZ = self.RA & self.RB  #and
            elif self.muxB == 1:
                self.RZ = self.RA & self.imm #andi
        elif operation == "sll":
            self.RZ = BitArray(int=self.RA, length=32) << self.RB
            self.RZ = self.RZ.int
        elif operation == "slt":
            if self.RA < self.RB :
                self.RZ = 1
            else :
                self.RZ = 0
        elif operation == "jalr":
            self.PC_temp = self.PC
            self.PC = self.RA + self.imm
        elif operation == "beq":
            if self.RA == self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "bge":
            if self.RA >= self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "blt":
            if self.RA < self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "bne":
            if self.RA != self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "auipc":
            self.RZ = self.PC - 4 + self.imm
        elif operation == "jal":
            self.PC_temp = self.PC
            self.PC = self.PC - 4 + self.imm
        else :
            print("no operation found in the AlU part")

        self.memoryAccess()

    def memoryAccess(self):
        print("\n|--------Memory accessing of the instruction---------------|\n")

        # for load and store part in instruction
        if self.memory_enable:
            if self.muxY == 1:
                if self.funct3 == "010":
                    self.data = self.Memory.readWord(self.RZ)   #lw
                elif self.funct3 == "000":
                    self.data = self.Memory.readByte(self.RZ)   #lb
                elif self.funct3 == "001":
                    self.data = self.Memory.readDoubleByte(self.RZ)   #lh
            else:
                if self.funct3 == "010":                        #sw
                    self.Memory.writeWord(self.RZ,self.RM)
                elif self.funct3 == "000":                      #sb
                    self.Memory.writeByte(self.RZ,self.RM)
                elif self.funct3 == "001":                      #sh
                    self.Memory.writeDoubleByte(self.RZ, self.RM)

        #writing in  muxY
        if self.muxY == 0:  #alu add addi
            self.RY = self.RZ
        elif self.muxY == 1: #load
            self.RY = self.data
        elif self.muxY == 2:    #store
            self.RY = self.PC_temp
        self.writeRegistor()

    def writeRegistor(self):
        print("\n|--------Write Back of instruction--------|\n")
        if self.write_enable:
            self.Register.update(self.RD, self.RY)
            print("RY:"+str(self.RY))


class register :
    #intializing the registor part
    def __init__(self):
        self.registers = {}
        for i in range (32) :
            self.registers['{0:05b}'.format(i)] = 0

    # for reading the value of the registor
    def read(self,address):
        return self.registers[address]

    #for updating the value of the registors
    def update(self,address,value):
        if not address=="00000":
            self.registers[address] = value

    # for returning the regestors file
    def returns(self):
        return self.registers

    # for earsing the value stored in the registors
    def flush(self):
        for i in range(32):
            self.registers['{0:05b}'.format(i)] = 0

class memory:
    def __init__(self):
        self.memory = {}

    # for writing the word in the memory
    def writeWord(self,address,value):

        value = BitArray(int = value, length = 32).bin
        self.memory[address] = value[24:32]
        self.memory[address+1] = value[16:24]
        self.memory[address+2] = value[8:16]
        self.memory[address+3] = value[0:8]

    # for writing the Byte in the memory
    def writeByte(self,address,value):

        value = BitArray(int = value, length = 8).bin
        self.memory[address] = value

    # for writing the Double Byte in the memory
    def writeDoubleByte(self,address,value):

        value = BitArray(int = value, length = 32).bin
        self.memory[address] = value[24:32]
        self.memory[address+1] = value[16:24]

    # for reading the word from memory
    def readWord(self,address):
        data = ""
        for i in range(4):
            if address+i in self.memory:
                data = self.memory[address+i] + data
            else:
                data = "00000000" + data
        return BitArray(bin = data).int

    # for reading the byte from the memory
    def readByte(self,address):
        if address in self.memory:
            return BitArray(bin = self.memory[address]).int
        else:
            return 0

    # for reading the double byte from the memory
    def readDoubleByte(self, address):
        data = ""
        for i in range(2):
            if address+i in self.memory:
                data = self.memory[address+i] + data
            else:
                data = "00000000" + data
        return BitArray(bin = data).int

    

    # for returning the memory
    def returns(self):
        return self.memory

    #for making the memory empty
    def flush(self):
        self.memory.clear()


if __name__ == "__main__":
    programRun()
