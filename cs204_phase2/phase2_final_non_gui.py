from bitstring import BitArray
import json,sys


def Run_program():
    print("Selct 1 for Non-pipelined")
    print("Selct 2 for pipelined")
    print("Selct 3 for Non-pipelined")

    choice = int(input("please enter your choice : "))

    if choice == 1 :
        print("/---------Non-Pipelined Running-------------/\n")
        Execute = execute()
        machine_file = open("code.mc", "r")
        MC = machine_file.read()
        machine_file.close()
        print(MC)
        if(MC!=""):
            Execute.Store_instruction(MC)
            Execute.Code_run()
            memory = Execute.Memory.returns()
            data ={}
            for i in memory :
                data[hex(i)] = memory[i]
            with open('memory.mc', 'w') as outfile:
                json.dump(data, outfile, indent=4)
            print("No. of Cycles taken to execute the program : "+str(Execute.cycle))


        else:
            print("Input Valid mc code")
        #except:
            #print("Input Valid mc code")
    else :

        Execute = pipelineExecute()
        if choice == 2 :
            Execute.do_dataForwarding = 0
            print("/---------Pipelined Running-------------/\n")
        else :
            Execute.do_dataForwarding = 1
            print("/---------Pipelined with DF Running-------------/\n")

        machine_file = open("code.mc", "r")
        MC = machine_file.read()
        machine_file.close()
        print(MC)
        #try:
        if(MC!=""):
            Execute.Store_instruction(MC)
            Execute.Code_run()
            memory = Execute.Memory.returns()
            data ={}
            for i in memory :
                data[hex(i)] = memory[i]
            with open('memory.mc', 'w') as outfile:
                json.dump(data, outfile, indent=4)
            #print("No. of Cycles taken to execute the program : "+str(Execute.cycle))

        else:
            print("Input Valids mc code")
        #except:
            #print("Input Valid mc code")


class execute :

    # initialinzing the code
    def __init__(self) :

        self.sp =0x7ffffff0
        """
            for creating the registor file
        """
        self.Register = register()  #creating register


        self.cycle = 0
        self.Register.update("00010", self.sp)
        self.Program_counter = 0

        """
            for creating the memory
        """
        self.Memory = memory()  #creating memory
        self.instruction = 0

    #  storing the instruction in the memory file
    def Store_instruction(self,MC):



        """
            this code is used for storing the given instruction in the memory
        """
        if (MC == None):
            return "no code provided"

        """
        spliting the machine code
        and storing in the list
        """
        MC = MC.splitlines()
        self.Memory.flush()
        self.Register.flush()
        for line in MC:
                try:
                    """
                    storing the given instructions in
                    the memory
                    """
                    address, instruction = line.split()
                    value = BitArray(hex=instruction).int
                    address = int(address,16)

                    self.Memory.writeWord(address,value)
                except:
                    return "some problem in storing the instruction in memory"

    """
      This function is for running the code
    """
    def Code_run(self) :

        print("\n|-----------State before the execution of the program -------------|\n")
        print("Register: ")
        print(self.Register.returns())
        print("Memory: ")
        print(self.Memory.returns())
        print("\n|-----------Execution of the program start-------|\n")
        while self.Memory.readWord(self.Program_counter) != 0:
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
        self.instruction = self.Memory.readWord(self.Program_counter)
        self.instruction = BitArray(int = self.instruction, length = 32).bin
        print("instruction:"+str(self.instruction))

        """
            Increase Program_counter for next instruction
        """
        self.Program_counter+=4

        """
            now going to the next step of execution
        """
        self.Decode()

    def checkFormat(self):

        # storing the part of the OP_code of every insstruction
        i_OR_s = ["0000011", "0001111", "0010011", "0011011", "0100011", "1100111", "1110011"]
        r = ["0110011", "0111011"]
        u = ["0010111", "0110111"]
        sb = "1100011"
        uj = "1101111"

        # checking the type

        if self.OP_code in r:
            return "r"
        elif self.OP_code in u:
            return "u"
        elif self.OP_code == sb:
            return "sb"
        elif self.OP_code == uj:
            return "uj"
        elif self.OP_code in i_OR_s:
            if self.OP_code == "0100011" and self.funtion_3 != "011":
                return "s"
            else:
                return "i"
        else :
            print("no Format match")
            return "none"

    def Decode(self):
        print("\n|--------------Decode of the instruction-------------|\n")

        """
            extracting the OP_code
        """
        self.OP_code = self.instruction[25:32]

        """
            checking the format of the instruction
        """
        print("OP_code:"+self.OP_code)

        """
            assigning all the control signals
        """
        self.memory_enable = 0
        self.write_enable = 1
        self.muxY = 0
        self.RZ = 0

        """
            checking the format
        """

        format = self.checkFormat()
        print("format", format)
        if format == "r":
            self.DecodeR()
            return
        if format == "i":
            self.DecodeI()
            return
        if format == "uj":
            self.DecodeUJ()
            return
        if format == "s":
            self.DecodeS()
            return
        if format == "u":
            self.DecodeU()
            return
        if format == "sb":
            self.DecodeSB()
            return

    def DecodeR(self):

        # Extracting the part of the instruction

        """
        extracting all the part in the instruction

        """

        self.funtion_7 = str(self.instruction[0:7])
        self.Sou = str(self.instruction[7:12])
        self.dest_reg_1 = str(self.instruction[20:25])
        self.source_reg_1 = str(self.instruction[12:17])
        self.RB = self.Register.read(self.Sou)  # Loading value of register at Sou
        self.RA = self.Register.read(self.source_reg_1)  # Loading value of register at rs1
        self.funtion_3 = str(self.instruction[17:20])
        self.muxY = 0
        """
            printing all the instruction data after the Decode done
        """
        print("RA", self.RA, "RB", self.RB, "dest_reg_1", self.dest_reg_1)

        # assigning the instruction to the ALU

        self.muxB = 0

        no_match_found = 1
        if self.funtion_3 == "110":
            if self.funtion_7 == "0000000":
                self.ALU("or")  # or
            elif self.funtion_7 == "0000001":
                self.ALU("rem")  # rem
            no_match_found = 0
        if self.funtion_3 == "100":
            if self.funtion_7 == "0000000":
                self.ALU("xor")  # xor
            elif self.funtion_7 == "0000001":
                self.ALU("div")  # div
            no_match_found = 0
        if self.funtion_3 == "000":
            if self.funtion_7 == "0000000":
                self.ALU("add")  # add
            if self.funtion_7 == "0000001":
                self.ALU("mul")  # mul
            if self.funtion_7 == "0100000":
                self.ALU("sub")  # sub
            no_match_found = 0
        if self.funtion_3 == "111" and self.funtion_7 == "0000000":
            self.ALU("and")  # and
            no_match_found = 0
        if self.funtion_3 == "001" and self.funtion_7 == "0000000":
            self.ALU("sll")  # sll
            no_match_found = 0
        if self.funtion_3 == "010" and self.funtion_7 == "0000000":
            self.ALU("slt")  # slt
            no_match_found = 0
        if self.funtion_3 == "101":
            if self.funtion_7 == "0000000":
                self.ALU("srl")  # srl
            if self.funtion_7 == "0100000":
                self.ALU("sra")  # sra
            no_match_found = 0
        if (no_match_found):
            print("No match found in the R format")

    def DecodeI(self):

        self.muxB = 1

        # extracting all the feilds of the instruction

        """
            extracting all the part in the instruction
        """
        self.imm = BitArray(bin = self.instruction[0:12]).int
        self.source_reg_1 = str(self.instruction[12:17])
        self.RA = self.Register.read(self.source_reg_1)
        self.funtion_3 = str(self.instruction[17:20])
        self.dest_reg_1 = str(self.instruction[20:25])

        """

            printing all the part in the instruction

        """
        no_match_found=1
        print("source_reg_1:"+self.source_reg_1)
        print("imm:"+str(self.imm))
        print("dest_reg_1:"+self.dest_reg_1)
        print("funtion_3:"+self.funtion_3)
        print("RA:"+str(self.RA))
        # assigning the instruction to the ALU

        And="and"
        Or="or"
        ADD="add"
        Jalr="jalr"

        if self.OP_code == "0010011" and self.funtion_3 == "111":
                no_match_found=0
                self.muxY = 0
                self.ALU(And)             #andi
        if self.OP_code == "0010011" and self.funtion_3 == "110":
                no_match_found=0
                self.muxY = 0
                self.ALU(Or)             #ori
        if self.OP_code == "1100111" and self.funtion_3 == "000":
            no_match_found=0
            self.muxY=2
            self.ALU(Jalr)                #jalr
        if self.OP_code == "0010011" and self.funtion_3 == "000":
            no_match_found=0
            self.muxY = 0
            self.ALU(ADD) #addi
        if self.OP_code == "0000011" and self.funtion_3 == "010"  :
            self.memory_enable=1
            no_match_found=0
            self.muxY=1
            self.ALU(ADD)    #all load ins lb, lh, lw
        if self.OP_code == "0000011":
            if(self.funtion_3 == "000" or self.funtion_3 == "001" or self.funtion_3 == "101" or self.funtion_3 == "100"):
                self.memory_enable=1
                no_match_found=0
                self.muxY=1
                self.ALU(ADD)    #all load ins lb, lh, lw

        if(no_match_found):
            print("No match found in I-format\n")

    def DecodeS(self):
        # extracting all the feilds of the instruction

        """

        extracting all the parts persent in the instruction

        """
        self.Sou = str(self.instruction[7:12])
        self.RB = self.Register.read(self.Sou)
        self.source_reg_1 = str(self.instruction[12:17])
        self.funtion_3 = str(self.instruction[17:20])
        self.RA = self.Register.read(self.source_reg_1)
        """
            extractacting the immidate field from the instruction
        """
        imm2 = str(self.instruction[20:25])
        imm1 = str(self.instruction[0:7])

        """
        assigning the control signals
        """
        self.write_enable = 0
        self.imm = BitArray(bin = imm1+imm2).int

        print("source_reg_1:",self.source_reg_1)
        print("Sou:",self.Sou)
        print("RA:",self.RA)
        print("RB:",self.RB)
        print("funtion_3:",self.funtion_3)

        # assigning the instruction to the ALU
        """
            NOW FOR THE STORE INSTRUCTION
        """
        if self.funtion_3 == "000" :
            self.muxB = 1
            self.RM = self.RB
            self.memory_enable = 1
            self.ALU("add")
        elif self.funtion_3 == "001" or self.funtion_3 == "010":
            self.muxB = 1
            self.RM = self.RB
            self.memory_enable = 1
            self.ALU("add")

        else :
            print("No match found in S format")

    def DecodeSB(self):

        # Exxtracting the part of the instruction
        self.funtion_3 = str(self.instruction[17:20])
        self.Sou = str(self.instruction[7:12])
        self.source_reg_1 = str(self.instruction[12:17])
        self.RB = self.Register.read(self.Sou)
        self.RA = self.Register.read(self.source_reg_1)

        """
            printing the result

        """
        print("source_reg_1:"+self.source_reg_1)
        print("Sou:"+self.Sou)

        imm4 = str(self.instruction[20:24])
        imm3 = str(self.instruction[1:7])
        imm2 = str(self.instruction[24])
        imm1 = str(self.instruction[0])
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int

        print("RA:"+str(self.RA))
        print("RB:"+str(self.RB))

        """
            assgining the value of the control signal
        """
        self.write_enable = 0
        self.muxB = 0
        no_match_found = 1
        # assigning the instruction to the ALU
        if self.funtion_3 == "001":
            self.ALU("bne")                 #bne
            no_match_found = 0
        if self.funtion_3 == "100":
            self.ALU("blt")                 #blt
            no_match_found = 0
        if self.funtion_3 == "101":
            self.ALU("bge")                 #bge
            no_match_found = 0
        if self.funtion_3 == "000":
            self.ALU("beq")                 #beq
            no_match_found = 0
        if (no_match_found):
            print("No match found in SB format")

    def DecodeU(self):

        # extracting all the part of the instruction

        imm1 = self.instruction[0:20]
        self.dest_reg_1 = self.instruction[20:25]
        self.imm=BitArray(bin=imm1+"000000000000").int

        print("dest_reg_1:"+self.dest_reg_1)


        # assigning the instruction to the ALU
        if self.OP_code!="0110111":
            self.ALU("auipc")       #auipc

        else:
            self.muxB=1
            self.RA=0
            self.ALU("add")          #lui

    def DecodeUJ(self):


        imm1 = str(self.instruction[0])
        imm4 = str(self.instruction[1:11])
        imm3 = str(self.instruction[11])
        imm2 = str(self.instruction[12:20])
        self.dest_reg_1 = str(self.instruction[20:25])

        print("dest_reg_1:"+self.dest_reg_1)

        self.muxY=2
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int
        self.ALU("jal")

    def ALU(self,operation):
        print("\n|--------- (ALU Part)Execution of the instruction----------|\n")
        print("OP:",operation)
        no_match_found = 1
        if operation == "xor":
            no_match_found = 0
            self.RZ = self.RA ^ self.RB
            
        if operation == "add":
            no_match_found = 0
            if self.muxB == 1:
                self.RZ = self.RA + self.imm  #addi
            elif self.muxB == 0:
                self.RZ = self.RA + self.RB   #add
            
        if operation == "mul":
            no_match_found = 0
            self.RZ = self.RA * self.RB
            
        if operation == "div":
            no_match_found = 0
            self.RZ = self.RA // self.RB
            
        if operation == "rem":
            no_match_found = 0
            self.RZ = self.RA % self.RB
            
        if operation == "or":
            no_match_found = 0
            if self.muxB == 1:
                self.RZ = self.imm or self.RA  #ori
            elif self.muxB == 0:
                self.RZ = self.RB or self.RA   #or
            
        if operation == "sra":
            no_match_found = 0
            self.RZ = self.RA >> self.RB
            
        if operation == "srl":
            no_match_found = 0
            self.RZ = BitArray(int=self.RA, length=32) >> self.RB
            self.RZ = self.RZ.int

        if operation == "sll":
            no_match_found = 0

            self.RZ = BitArray(int=self.RA, length=32) << self.RB
            
            self.RZ = self.RZ.int

        if operation == "sub":
            no_match_found = 0
            self.RZ = self.RA - self.RB
            
        if operation == "and":
            no_match_found = 0

            if self.muxB == 1:
                self.RZ = self.imm and self.RA #andi
            
            if self.muxB == 0:
                self.RZ = self.RA and self.RB  #and

        if operation == "jalr":
            no_match_found = 0
            self.PC_temp = self.Program_counter
            self.Program_counter = self.RA + self.imm
            

        if operation == "slt":
            no_match_found = 0
            if self.RB > self.RA :
                self.RZ = 1
            else :
                self.RZ = 0
            

        if operation == "bge":
            no_match_found = 0

            if self.RA >= self.RB:
                self.Program_counter = self.imm + self.Program_counter - 4

        if operation == "jal":
            no_match_found = 0
            self.PC_temp = self.Program_counter
            
            self.Program_counter = self.imm + self.Program_counter - 4

        if operation == "auipc":
            no_match_found = 0
            self.RZ = self.Program_counter + self.imm - 4
            

        if operation == "bne":
            no_match_found = 0
            if self.RA != self.RB:
                self.Program_counter = self.Program_counter + self.imm -4
            

        if operation == "blt":
            no_match_found = 0
            if self.RA < self.RB:
                self.Program_counter = self.imm + self.Program_counter - 4
            

        if operation == "beq":
            no_match_found = 0
            if self.RA == self.RB:
                self.Program_counter = self.Program_counter + self.imm - 4
            

        if (no_match_found) :
            print("no operation found in the AlU part")

        self.memoryAccess()

    def memoryAccess(self):


        # for load and store part in instruction
        print("\n|--------Memory accessing of the instruction---------------|\n")
        if self.memory_enable:
            if self.muxY ==1 and self.funtion_3 == "010":
                self.data = self.Memory.readWord(self.RZ)   #lw

            if self.muxY !=1 and self.funtion_3 == "010":
                self.Memory.writeWord(self.RZ,self.RM)

            if self.muxY ==1 and self.funtion_3 == "000":
                self.data = self.Memory.readByte(self.RZ)   #lb

            if self.muxY !=1 and self.funtion_3 == "000":
                self.Memory.writeByte(self.RZ,self.RM)

            if self.muxY ==1 and self.funtion_3 == "001":
                self.data = self.Memory.readDoubleByte(self.RZ)   #lh

            if self.muxY !=1 and self.funtion_3 == "001":
                self.Memory.writeDoubleByte(self.RZ, self.RM)


        if self.muxY == 1: #load
            self.RY = self.data

        if self.muxY == 0:  #ALU add addi
            self.RY = self.RZ

        if self.muxY == 2:    #store
            self.RY = self.PC_temp



        self.writeRegistor()

    def writeRegistor(self):
        print("\n|--------Write Back of instruction--------|\n")
        if self.write_enable:
            self.Register.update(self.dest_reg_1, self.RY)
            print("RY:"+str(self.RY))


class pipelineExecute :

    def __init__ (self) :
        self.sp=0x7ffffff0                              # for the stack pointer
        self.Program_counter = 0                                     # program counter
        self.instruction = 0                            # for the instruction
        self.RY = 0

        self.stall_counter = self.data_stalling_count = 0
        self.imm = 0                                    # for the immidate field

        self.do_dataForwarding = 1                   # for checking if data forwarding is allowed or not

        self.RDQueue = []                               #Queue to store dest_reg_1(s) from all the instruction from proper pipeling
        self.branchTaken = 0


        """

        for storing the count to print in the instruction result.


        """
        self.count_instructions = self.total_control_ins = self.total_data_ins = self.ALU_instruction_count = 0
        self.cycle =self.old_data_hazard=self.data_hazards = self.control_hazards = 0                        #For counting purposes
                           
        


        
        

        # for stopping the Code_run of the program
        

        """
        parameters for executing functions

        """
                           # for the output registor
        
        self.fetch_run =self.Decode_run =self.alu_run =self.MEM_access_prog = 0
        self.stopPipeLine=0
                                             
        self.Register = register()                      # for the registor file
        self.Memory = memory()                          # for the memory
        self.RM =self.RZ =self.RB =self.RA = 0                                     # for the input1 registor
                                            


    #  storing the instruction in the memory file
    def Store_instruction(self,MC):



        """
            this code is used for storing the given instruction in the memory
        """
        if (MC == None):
            return "no code provided"

        """
        spliting the machine code
        and storing in the list
        """
        MC = MC.splitlines()
        self.Memory.flush()
        self.Register.flush()
        for line in MC:
                try:
                    """
                    storing the given instructions in
                    the memory
                    """
                    address, instruction = line.split()
                    value = BitArray(hex=instruction).int
                    address = int(address,16)

                    self.Memory.writeWord(address,value)
                except:
                    return "some problem in storing the instruction in memory"


    def Code_run(self) :

        print("\n|-----------State before the execution of the program -------------|\n")
        print("Register: ")
        print(self.Register.returns())
        print("Memory: ")
        print(self.Memory.returns())
        print("\n|-----------Execution of the program start-------|\n")

        while not self.stopPipeLine :
            self.runPipeLine()

        print("\n-------After Execution of the program -------\n")

        print("Register: ")
        print(self.Register.returns())
        print("Memory: ")
        print(self.Memory.returns())
        print()
        print()
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("DETAILS OF THE CODE")
        print("Number of the Cyle taken =", self.cycle)
        print("Number of the instruction executed =", self.count_instructions)
        print("Cycle Per Instruction (CPI) =", self.cycle/self.count_instructions)
        print("Number of Data-transfer (load and store) instructions executed =", self.total_data_ins)
        print("Number of ALU instructions executed =", self.ALU_instruction_count)
        print("Number of Control instructions executed =", self.control_hazards)
        print("Number of stalls/bubbles in the pipeline =", self.data_stalling_count)
        print("Number of data hazards =", self.data_hazards)
        print("Number of control hazards =", self.control_hazards)
        print("Number of branch mispredictions = ", self.stall_counter)
        print("Number of stalls due to data hazards =", self.data_stalling_count)
        print("Number of stalls due to control hazards =", self.stall_counter)

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    def runPipeLine(self) :

        #printing how many cycle completed
        print('Cycle No. : '+ str(self.cycle))

        """

        for the instruction in which memory execution is completed

        """
        if self.MEM_access_prog:
            self.Reg_write()

        """

        for the instruction in which the ALU execution is completed

        """
        if self.alu_run:
            self.memAccess()
        else:
            self.MEM_access_prog = 0

        """

        for the instruction in which the Decoding is completed

        """
        if self.Decode_run:
            self.ALU()
        else:
            self.alu_run = 0

        """

        for the instruction in which the Fetching is completed

        """
        if self.fetch_run:
            self.Decode()
        else:
            self.Decode_run = 0

        """

        Now fetching the next instruction

        """

        if self.Memory.readWord(self.Program_counter) != 0:
            self.fetch()
        else:
            self.fetch_run = 0

        """

        Increasing the number of cycle

        """
        self.cycle = self.cycle+1


        """

        for stopping the instruction

        """

        if (self.Memory.readWord(self.Program_counter) == 0) and (not self.fetch_run) and (not self.alu_run) and (not self.MEM_access_prog)  and (not self.Decode_run) :
            print('PipeLine Stoped!')
            self.stopPipeLine = 1


    # for fetching the instruction

    def fetch(self):

        # making ready fetch
        self.fetch_run = 1
        self.instruction = self.Memory.readWord(self.Program_counter)
        self.instruction = BitArray(int = self.instruction, length = 32).bin
        print("instruction", self.instruction)
        self.Program_counter+=4



    # for checking the format
    def checkFormat(self):

        # storing the part of the OP_code of every insstruction
        i_OR_s = ["0000011", "0001111", "0010011", "0011011", "0100011", "1100111", "1110011"]
        r = ["0110011", "0111011"]
        u = ["0010111", "0110111"]
        sb = "1100011"
        uj = "1101111"

        # checking the type
        if self.OP_code in r:
            return "r"
        elif self.OP_code in u:
            return "u"
        elif self.OP_code == sb:
            return "sb"
        elif self.OP_code == uj:
            return "uj"
        elif self.OP_code in i_OR_s:
            if self.OP_code == "0100011" and self.funtion_3 != "011":
                return "s"
            else:
                return "i"
        else :
            print("no Format match")
            return "none"

    # for decoding the instruction
    def Decode(self) :

        """
            taking the buffer if anything persent
        """

        try:
            self.preload = self.Decode_buffer['load']
        except:
            self.preload = 0

        """
            intiating the buffer
        """

        self.Decode_buffer = {'dest_reg_1' : '-1','mem_enable' : '-1', 'load' : 0,  'muxY' : 0} #Decode buffer to store previous instruction gone through this stage

        self.Decode_run = 1


        """
            storing the OP_code
        """

        self.OP_code = self.instruction[25:32]


        # checking the format of the instruction
        format = self.checkFormat()

        # assigning all the control signals

        if format == "r":
            self.DecodeR()
            return
        if format == "i":
            self.DecodeI()
            return
        if format == "uj":
            self.DecodeUJ()
            return
        if format == "s":
            self.DecodeS()
            return
        if format == "u":
            self.DecodeU()
            return
        if format == "sb":
            self.DecodeSB()
            return


    def DecodeR(self):

        self.Sou = self.instruction[7:12]
        dest_reg_1 = self.instruction[20:25]
        self.RB = self.Register.read(self.Sou)  # Loading value of register at Sou
        self.funtion_7 = self.instruction[0:7]
        self.source_reg_1 = self.instruction[12:17]
        self.muxB = 0
        self.RA = self.Register.read(self.source_reg_1)  # Loading value of register at rs1
        self.funtion_3 = self.instruction[17:20]

        if self.Sou in self.RDQueue or self.source_reg_1 in self.RDQueue :    #checking if rs1 and Sou are in being used as rd for some other instruction

            if self.do_dataForwarding== 1:
                first = self.RDQueue[-1]
                if self.source_reg_1 == first:
                    self.old_data_hazard = 1
                    self.RA = self.RZ

                if self.Sou == first:
                    self.old_data_hazard = 1
                    self.RB = self.RZ

                try:
                    second = self.RDQueue[-2]
                    if first != second:

                        if self.source_reg_1 == second:
                            self.old_data_hazard = 1
                            self.RA = self.RY

                        if self.Sou == second:
                            self.old_data_hazard = 1
                            self.RB = self.RY
                except:
                    pass
            else:

                self.data_stalling_count = self.data_stalling_count + 1
                self.old_data_hazard = 1
                self.Program_counter = self.Program_counter - 4
                self.Decode_run = 0
                return

        if self.old_data_hazard:
            self.data_hazards = self.data_hazards + 1
            self.old_data_hazard = 0

        self.Decode_buffer['dest_reg_1'] = dest_reg_1   #updating Decode buffer for hazard manipulation
        #self.muxY=0
        self.ALU_instruction_count = self.ALU_instruction_count + 1 #instruction count update
        self.RDQueue.append(dest_reg_1)  # updating dest_reg_1 in queue for future data forwarding


        if self.funtion_3 == "000":
            if self.funtion_7 == "0000000":
                self.Decode_buffer['op'] = ("add")  # add
            elif self.funtion_7 == "0000001":
                self.Decode_buffer['op'] = ("mul")  # mul
            elif self.funtion_7 == "0100000":
                self.Decode_buffer['op'] = ("sub")  # sub
        elif self.funtion_3 == "110":
            if self.funtion_7 == "0000000":
                self.Decode_buffer['op'] = ("or")  # or
            elif self.funtion_7 == "0000001":
                self.Decode_buffer['op'] = ("rem")  # rem
        elif self.funtion_3 == "100":
            if self.funtion_7 == "0000000":
                self.Decode_buffer['op'] = ("xor")  # xor
            elif self.funtion_7 == "0000001":
                self.Decode_buffer['op'] = ("div")  # div
        elif self.funtion_3 == "101":
            if self.funtion_7 == "0000000":
                self.Decode_buffer['op'] = ("srl")  # srl
            elif self.funtion_7 == "0100000":
                self.Decode_buffer['op'] = ("sra")  # sra
        elif self.funtion_3 == "111" and self.funtion_7 == "0000000":
            self.Decode_buffer['op'] = ("and")  # and
        elif self.funtion_3 == "001" and self.funtion_7 == "0000000":
            self.Decode_buffer['op'] = ("sll")  # sll
        elif self.funtion_3 == "010" and self.funtion_7 == "0000000":
            self.Decode_buffer['op'] = ("slt")  # slt
        else :
            print("No match found in the R format")


    def DecodeI(self) :
        self.source_reg_1 = self.instruction[12:17]
        self.RA = self.Register.read(self.source_reg_1)
        '''load the first 12 bits of instruction in immediate value
        '''
        self.imm = BitArray(bin = self.instruction[0:12]).int
        ''' load dest_reg_1
        '''
        dest_reg_1 = self.instruction[20:25]
        ''' load the bits from 17 to 20 in func3
        '''
        self.funtion_3 = self.instruction[17:20]

        if self.source_reg_1 in self.RDQueue:
            ''' Check if data forwarding is 1 or not
            '''
            if self.do_dataForwarding == 1:
                first = self.RDQueue[-1]
                ''' Check if source_reg_1 is equal to first or not
                '''
                if self.source_reg_1 == first:
                    self.old_data_hazard = 1
                    self.RA = self.RZ

                try:
                    second = self.RDQueue[-2]
                    ''' Check if source_reg_1 is equal to second or not
                    '''
                    if first != second:
                        if self.source_reg_1 == second:
                            self.old_data_hazard = 1
                            self.RA = self.RY
                except:
                    pass
            else:
                ''' Decreasee Program_counter by 4
                 '''
                self.Program_counter = self.Program_counter - 4
                #print('Stalling!')
                self.data_stalling_count += 1
                ''' Set old_data_hazard equal to 1
                '''
                self.old_data_hazard = 1
                ''' Set Decode_run equal to 0'''
                self.Decode_run = 0

                return
        ''' Check if there was a data hazard or not
        '''
        if self.old_data_hazard == 1:
            '''  Set old_data_hazard equal to 0
            '''
            self.old_data_hazard = 0
            ''' As there was a data hazard, therefore increment data hazard by 1'''
            self.data_hazards+= 1


        self.Decode_buffer['dest_reg_1'] = dest_reg_1
        self.muxB = 1
        self.RDQueue.append(dest_reg_1)
        if self.OP_code == "0000011":
            if(self.funtion_3 == "000" or self.funtion_3 == "001" or self.funtion_3 == "010"  or self.funtion_3 == "100" or self.funtion_3 == "101" ):

                    '''change Decode_buffer['op'] to add
                    '''
                    self.Decode_buffer['op'] = 'add'
                    self.Decode_buffer['muxY'] = 1
                    self.Decode_buffer['load'] = 1
                    if self.funtion_3 == "010":
                        self.Decode_buffer['mem_enable'] = 'lw'     #lw
                    elif self.funtion_3 == "001":
                        self.Decode_buffer['mem_enable'] = 'lh'     #lh
                    elif self.funtion_3 == "000":
                        self.Decode_buffer['mem_enable'] = 'lb'     #lb
        elif self.OP_code == "0010011" and self.funtion_3 == "000":
            self.Decode_buffer['op'] = 'add'                 #addi
            self.ALU_instruction_count = self.ALU_instruction_count + 1
        elif self.OP_code == "1100111" and self.funtion_3 == "000":
            self.Decode_buffer['muxY'] = 2
            self.Decode_buffer['op'] = 'jalr'               #jalr
            self.total_control_ins += 1
            self.Program_counter = self.imm + self.RA
            self.Decode_buffer['PC_temp'] = self.Program_counter


        elif self.OP_code == "0010011":
            self.ALU_instruction_count += 1
            if self.funtion_3 == "110":
                self.Decode_buffer['op'] = 'ori'          #ori
            elif self.funtion_3 == "111":
                '''set Decode_buffer['op'] to 'andi'
                 '''
                self.Decode_buffer['op'] = 'andi'         #andi

    def DecodeS(self) :
        imm1 = self.instruction[0:7]
        self.Sou = self.instruction[7:12]
        self.RB = self.Register.read(self.Sou)

        self.source_reg_1 = self.instruction[12:17]
        self.RA = self.Register.read(self.source_reg_1)

        self.funtion_3 = self.instruction[17:20]
        imm2 = self.instruction[20:25]


        self.imm = BitArray(bin = imm1+imm2).int

        print("source_reg_1: ",self.source_reg_1)
        print("Sou: ",self.Sou)
        print("RA: ",self.RA)
        print("RB: ",self.RB)
        print("imm: ",self.imm)

        if self.Sou in self.RDQueue or self.source_reg_1 in self.RDQueue :
            if self.do_dataForwarding:
                first = self.RDQueue[-1]

                if self.Sou == first:
                    self.old_data_hazard = 1
                    self.RB = self.RZ

                if self.source_reg_1 == first:
                    self.old_data_hazard = 1
                    self.RA = self.RZ

                try:
                    second = self.RDQueue[-2]
                    if first != second:
                        if self.Sou == second:
                            self.old_data_hazard = 1
                            self.RB = self.RY

                        if self.source_reg_1 == second:
                            self.old_data_hazard = 1
                            self.RA = self.RY

                except:
                    pass
            else:

                self.data_stalling_count = self.data_stalling_count + 1
                self.old_data_hazard = 1
                self.Decode_run = 0
                self.Program_counter = self.Program_counter - 4
                return

        if self.old_data_hazard:
            self.old_data_hazard = 0
            self.data_hazards = self.data_hazards + 1

        self.RDQueue.append('-1')

        if self.funtion_3 == "000" or self.funtion_3 == "010" or self.funtion_3 == "001":

            self.Decode_buffer['op'] = 'add'
            self.muxB = 1

            if self.funtion_3 == "001":  # sh
                ''' set value of Decode_buffer ['mem_enable'] equal to sh
                '''
                self.Decode_buffer['mem_enable'] = 'sh'
            elif self.funtion_3 == "000":                      #sb
                ''' set value of Decode_buffer ['mem_enable'] equal to sb
                '''
                self.Decode_buffer['mem_enable'] = 'sb'
            elif self.funtion_3 == "010":                        #sw
                ''' set value of Decode_buffer ['mem_enable'] equal to sw
                '''
                self.Decode_buffer['mem_enable'] = 'sw'






    def DecodeSB(self) :

        imm1 = self.instruction[0]
        imm3 = self.instruction[1:7]
        self.Sou = self.instruction[7:12]
        self.source_reg_1 = self.instruction[12:17]
        self.funtion_3 = self.instruction[17:20]
        imm4 = self.instruction[20:24]
        imm2 = self.instruction[24]

        self.RB = self.Register.read(self.Sou)
        self.RA = self.Register.read(self.source_reg_1)
        '''Extracting the value of immediate from the instruction
        '''

        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int

        if self.Sou in self.RDQueue or self.source_reg_1 in self.RDQueue:
            if self.do_dataForwarding==1:
                reversedQueue = list(reversed(self.RDQueue))
                first = reversedQueue[0]
                ''' check if Sou is first or not
                '''
                if self.Sou == first:
                    self.old_data_hazard = 1
                    self.RB = self.RZ
                if self.source_reg_1 == first:
                    self.old_data_hazard = 1
                    self.RA = self.RZ
                try:
                    second = reversedQueue[1]
                    ''' Check if first is equal to second or not
                    '''
                    if first != second:
                        '''Check if value of Sou is equal to second or not
                        '''
                        if self.Sou == second:
                            self.old_data_hazard = 1
                            self.RB = self.RY
                        if self.source_reg_1 == second:
                            self.old_data_hazard = 1
                            self.RA = self.RY
                except:
                    pass
            else:
                self.data_stalling_count = self.data_stalling_count + 1
                self.Program_counter = self.Program_counter - 4
                self.Decode_run = 0
                self.old_data_hazard = 1
                return
        if self.old_data_hazard==1:
            ''' increment number of data hazards by 1
            '''
            self.data_hazards+= 1
            ''' change old_data_hazard to 0
            '''
            self.old_data_hazard = 0
        ''' increment total_control_ins and control_harzards by 1
        '''
        self.total_control_ins += 1
        self.control_hazards += 1 

        self.muxB = 0
        self.RDQueue.append('-1')

        if self.funtion_3 == "001":
            '''set value of Decode_buffer['op'] equal to bne
            '''
            self.Decode_buffer['op'] = 'bne'
        elif self.funtion_3 == "100":
            '''set value of Decode_buffer['op'] equal to blt
            '''
            self.Decode_buffer['op'] = 'blt'
        elif self.funtion_3 == "101":
            '''set value of Decode_buffer['op'] equal to bge
            '''
            self.Decode_buffer['op'] = 'bge'
        elif self.funtion_3 == "000":
            '''set value of Decode_buffer['op'] equal to beq
            '''
            self.Decode_buffer['op'] = 'beq'

    def DecodeU(self) :
        imm1 = self.instruction[0:20]
        dest_reg_1 = self.instruction[20:25]
        self.Decode_buffer['dest_reg_1']=dest_reg_1
        self.RDQueue.append(dest_reg_1)



        self.ALU_instruction_count=self.ALU_instruction_count+1
        self.imm=BitArray(bin=imm1+"000000000000").int
        add="add"
        auipc="auipc"
        if self.OP_code!= "0110111":
            self.Decode_buffer['op'] =auipc

        else:
            self.Decode_buffer['op'] =add
            self.RA = 0
            self.RB =self.RA
            self.muxB =self.RB+1

    def DecodeUJ(self) :
        self.total_control_ins=self.total_control_ins + 1
        self.RB =0
        self.RA =self.RB
        imm1 = self.instruction[0]
        imm4 = self.instruction[1:11]
        dest_reg_1 = str(self.instruction[20:25])
        self.Decode_buffer['dest_reg_1'] = dest_reg_1
        self.RDQueue.append(dest_reg_1)
        imm3 = str(self.instruction[11])
        imm2 = str(self.instruction[12:20])

        self.Decode_buffer['muxY'] = 2
        self.Decode_buffer['op']= 'jal'
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int


        self.Decode_buffer['PC_temp'] = self.Program_counter
        self.Program_counter=self.Program_counter + self.imm
        self.Program_counter =self.Program_counter - 4


    def ALU(self):
        self.alu_run = 1

        if self.do_dataForwarding==1:
            if self.preload==1:
                second = self.RDQueue[-2]
                if self.source_reg_1 == second:
                    self.cycle += 1 
                    self.data_stalling_count += 1
                    self.RA = self.RY
                try :
                    if self.Sou == second:
                        self.cycle += 1 
                        self.data_stalling_count += 1 
                        self.RB = self.RY
                except :
                    pass

        ''' Set value of RZ equal to 0
        '''
        self.RZ = 0
        ''' Set Value of memory_enable equal to value of Decode_buffer ['mem_enable']
        '''
        self.memory_enable = self.Decode_buffer['mem_enable']
        ''' Set Value of muxY equal to value of Decode_buffer ['muxY']
        '''
        self.muxY = self.Decode_buffer['muxY']

        self.alu_buffer = {'dest_reg_1' : self.Decode_buffer['dest_reg_1'], 'RM' : self.RB}
        ''' Set Value of operation '''
        operation = self.Decode_buffer['op']

        no_match_found  = 1
        if operation == "and":
            if self.muxB == 1:  #andi
                self.RZ = self.imm and self.RA
            no_match_found = 0
            if self.muxB == 0:  #and
                self.RZ = self.RB and self.RA

        if operation == "add":
            if self.muxB == 1:
                self.RZ = self.imm + self.RA #addi
            no_match_found = 0
            if self.muxB == 0:
                self.RZ = self.RB + self.RA #add
        if operation == "rem":
            self.RZ = self.RA % self.RB  # rem
            no_match_found = 0
        if operation == "div":
            self.RZ = self.RA // self.RB # div
            no_match_found = 0
        if operation == "mul":
            self.RZ = self.RB * self.RA  # mul
            no_match_found = 0
        if operation == "beq":
            if self.RA == self.RB:      # beq
                self.stall_counter += 1
                self.fetch_run = 0  #stalling whole cycle for hazard control
                self.Program_counter = self.Program_counter + self.imm - 4

            no_match_found = 0

        if operation == "jal":     #jal
            self.PC_temp = self.Decode_buffer['PC_temp']
            no_match_found = 0

        if operation == "slt": #slt
            if self.muxB == 0:
                if self.RA < self.RB:
                    self.RZ = 1
                else:
                    self.RZ=0
            no_match_found = 0

        if operation == "sra":
            self.RZ = self.RA >> self.RB
            no_match_found = 0
        if operation == "srl": #srl
            self.RZ = BitArray(int=self.RA, length=32) >> self.RB
            self.RZ = self.RZ.int
            no_match_found = 0
        if operation == "sll":  #sll
            self.RZ = BitArray(int=self.RA, length=32) << self.RB
            self.RZ = self.RZ.int
            no_match_found = 0
        if operation == "sub":   #sub
            self.RZ = self.RA - self.RB
            no_match_found = 0
        if operation == "xor":  #xor
            self.RZ = self.RA ^ self.RB
            no_match_found = 0
        if operation == "or":
            if self.muxB == 1:   #ori
                self.RZ = self.RA or self.imm
            if self.muxB == 0:   #or
                self.RZ = self.RA or self.RB
            no_match_found = 0
        if operation == "jalr":   #jalr
            self.PC_temp = self.Decode_buffer['PC_temp']
            #self.Program_counter = self.RA + self.imm
            no_match_found = 0
        if operation == "auipc":     #auipc
            self.RZ = self.Program_counter + self.imm - 4
            no_match_found = 0
        if operation == "blt":
            if self.RA < self.RB:      #blt
                self.stall_counter+=1
                self.Program_counter = self.imm  + self.Program_counter - 4
                self.fetch_run = 0
            no_match_found = 0
        if operation == "bne":        #bne
            if self.RA != self.RB:
                self.stall_counter+=1
                self.Program_counter = self.imm - 4 + self.Program_counter
                self.fetch_run = 0
            no_match_found = 0
        if operation == "bge":
            if self.RA >= self.RB:      #bge
                self.stall_counter+=1
                self.fetch_run = 0
                self.Program_counter =  self.imm + self.Program_counter - 4
            no_match_found = 0
        if (no_match_found) :
            print("no match in ALU")



    def memAccess(self):
        self.MEM_access_prog = 1

        self.RM = self.alu_buffer['RM']
        self.dest_reg_1 = self.alu_buffer['dest_reg_1']

        '''
        memory_enable is a control signal
        It is determined in Decode stage
        '''

        if self.memory_enable != '-1':
            self.total_data_ins +=  1

            no_match_found = 1

            if self.memory_enable == "sh":  # sh
                self.Memory.writeDoubleByte(self.RZ, self.RM)
                no_match_found = 0

            if self.memory_enable == "sw":  # sw
                self.Memory.writeWord(self.RZ, self.RM)
                no_match_found = 0

            if self.memory_enable == "lb":
                self.data = self.Memory.readByte(self.RZ)  # lb
                no_match_found = 0

            if self.memory_enable == "lh":
                self.data = self.Memory.readDoubleByte(self.RZ)  # lh
                no_match_found = 0

            if self.memory_enable == "sb":  # sb
                self.Memory.writeByte(self.RZ, self.RM)
                no_match_found = 0

            if self.memory_enable == "lw":
                self.data = self.Memory.readWord(self.RZ)  # lw
                no_match_found = 0
            if (no_match_found) :
                print("no match found in mem access")

        # writing in  muxY
        no_match_found = 1
        if self.muxY == 0:
            self.RY = self.RZ
            no_match_found = 0

        if self.muxY == 2:
            self.RY = self.PC_temp
            no_match_found = 0

        if self.muxY == 1:
            self.RY = self.data
            no_match_found = 0
        if (no_match_found) :
            print("problem in writing in mem access")

    def Reg_write(self):

        '''
        Since this is the write back stage
        this step marks the end of instruction execution
        write back is done only if dest_reg_1 is not -1
        This is decided in Decode stage
        '''

        self.count_instructions = self.count_instructions + 1

        if self.dest_reg_1 != '-1':
            self.Register.update(self.dest_reg_1, self.RY)

        '''
        To optimize finding of data hazard
        we remove the dest_reg_1 from RDQueue
        '''
        try:
            self.RDQueue = self.RDQueue[1:]

        except:
            pass


class register :
    #intializing the registor part
    def __init__(self):
        self.registers = {}
        for i in range (32) :
            x = '{0:05b}'.format(i)
            self.registers[x] = 0

    #for updating the value of the registors
    def update(self,address,value):
        if not address=="00000":
            self.registers[address] = value

    # for returning the regestors file
    def returns(self):
        return self.registers

    # for reading the value of the registor
    def read(self,address):
        return self.registers[address]

    # for earsing the value stored in the registors
    def flush(self):
        for i in range(32):
            x = '{0:05b}'.format(i)
            self.registers['{0:05b}'.format(i)] = 0


class memory:
    def __init__(self):
        self.memory ={}
    # for reading the byte from the memory
    def readByte(self,address):
        if address in self.memory:
            return BitArray(bin = self.memory[address]).int
        return 0

    # for writing the Byte in the memory
    def writeByte(self,address,value):

        value = BitArray(int =value,length=8).bin
        self.memory[address]=value

    def readWord(self,address):
        data_word=""

        leading_z="00000000"

        if address in self.memory:
                data_word = self.memory[address] + data_word

        else:
                data_word = leading_z + data_word
        if address+1  in self.memory:
                data_word = self.memory[address+1] + data_word

        else:
                data_word = leading_z + data_word
        if address+2  in self.memory:
                data_word = self.memory[address+2] + data_word

        else:
                data_word = leading_z + data_word
        if address+3  in self.memory:
                data_word = self.memory[address+3] + data_word

        else:
                data_word = leading_z + data_word



        return BitArray(bin = data_word).int

    # for writing the word in the memory
    def writeWord(self,address,value):

        value = BitArray(int = value, length = 32).bin
        for i in range(1,5):
            self.memory[address+i-1]=value[32-8*i:32-8*i+8]


        #for making the memory empty
    def flush(self):
        self.memory.clear()
    # for reading the word from memory




    # for reading the double byte from the memory
    def readDoubleByte(self, address):
        data =""
        for i in range(2):
            if address+i not in self.memory:
                data = "00000000" + data
            else:
                data = self.memory[address+i] + data
        return BitArray(bin = data).int

    # for writing the Double Byte in the memory
    def writeDoubleByte(self,address,value):

        value = BitArray(int = value, length = 32).bin
        self.memory[address] = value[24:32]
        self.memory[address+1] = value[16:24]



    # for returning the memory
    def returns(self):
        return self.memory
if __name__=="__main__":
    Run_program()


