from bitstring import BitArray
import json
from tkinter import *
from tkinter.font import Font

class GUI:
    def __init__(self,master):
        self.master=master
        self.master.title("RISC-V Simulator")
        self.master.config(bg="black")
        self.master.resizable(0,0)
        #---------------------Font------------------------
        self.default_font=Font(family="Helvetica",size=16)
        # self.button_font=Font(size=14)

        #################################### Canvas ##########################
        self.canvas = Canvas(self.master,width=500,height=700)
        self.frame = Frame(self.canvas,width=500,height=1320,bg="black")
        self.scroll_y = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)

        ######################## Labels ###############################
        self.x0_label= Label(self.frame,text="x0",fg="gold",bg="black",font=self.default_font)
        self.x0_label.place(x=50,y=20)
        self.entry0=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry0.place(x=100,y=25)


        self.x1_label= Label(self.frame,text="x1",fg="gold",bg="black",font=self.default_font)
        self.x1_label.place(x=50,y=60)
        self.entry1=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry1.place(x=100,y=65)


        self.x2_label= Label(self.frame,text="x2",fg="gold",bg="black",font=self.default_font)
        self.x2_label.place(x=50,y=100)
        self.entry2=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry2.place(x=100,y=105)


        self.x3_label= Label(self.frame,text="x3",fg="gold",bg="black",font=self.default_font)
        self.x3_label.place(x=50,y=140)
        self.entry3=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry3.place(x=100,y=145)


        self.x4_label= Label(self.frame,text="x4",fg="gold",bg="black",font=self.default_font)
        self.x4_label.place(x=50,y=180)
        self.entry4=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry4.place(x=100,y=185)


        self.x5_label= Label(self.frame,text="x5",fg="gold",bg="black",font=self.default_font)
        self.x5_label.place(x=50,y=220)
        self.entry5=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry5.place(x=100,y=225)


        self.x6_label= Label(self.frame,text="x6",fg="gold",bg="black",font=self.default_font)
        self.x6_label.place(x=50,y=260)
        self.entry6=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry6.place(x=100,y=265)


        self.x7_label= Label(self.frame,text="x7",fg="gold",bg="black",font=self.default_font)
        self.x7_label.place(x=50,y=300)
        self.entry7=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry7.place(x=100,y=305)


        self.x8_label= Label(self.frame,text="x8",fg="gold",bg="black",font=self.default_font)
        self.x8_label.place(x=50,y=340)
        self.entry8=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry8.place(x=100,y=345)


        self.x9_label= Label(self.frame,text="x9",fg="gold",bg="black",font=self.default_font)
        self.x9_label.place(x=50,y=380)
        self.entry9=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry9.place(x=100,y=385)


        self.x10_label= Label(self.frame,text="x10",fg="gold",bg="black",font=self.default_font)
        self.x10_label.place(x=50,y=420)
        self.entry10=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry10.place(x=100,y=425)


        self.x11_label= Label(self.frame,text="x11",fg="gold",bg="black",font=self.default_font)
        self.x11_label.place(x=50,y=460)
        self.entry11=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry11.place(x=100,y=465)


        self.x12_label= Label(self.frame,text="x12",fg="gold",bg="black",font=self.default_font)
        self.x12_label.place(x=50,y=500)
        self.entry12=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry12.place(x=100,y=505)


        self.x13_label= Label(self.frame,text="x13",fg="gold",bg="black",font=self.default_font)
        self.x13_label.place(x=50,y=540)
        self.entry13=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry13.place(x=100,y=545)


        self.x14_label= Label(self.frame,text="x14",fg="gold",bg="black",font=self.default_font)
        self.x14_label.place(x=50,y=580)
        self.entry14=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry14.place(x=100,y=585)


        self.x15_label= Label(self.frame,text="x15",fg="gold",bg="black",font=self.default_font)
        self.x15_label.place(x=50,y=620)
        self.entry15=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry15.place(x=100,y=625)


        self.x16_label= Label(self.frame,text="x16",fg="gold",bg="black",font=self.default_font)
        self.x16_label.place(x=50,y=660)
        self.entry16=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry16.place(x=100,y=665)


        self.x17_label= Label(self.frame,text="x17",fg="gold",bg="black",font=self.default_font)
        self.x17_label.place(x=50,y=700)
        self.entry17=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry17.place(x=100,y=705)


        self.x18_label= Label(self.frame,text="x18",fg="gold",bg="black",font=self.default_font)
        self.x18_label.place(x=50,y=740)
        self.entry18=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry18.place(x=100,y=745)


        self.x19_label= Label(self.frame,text="x19",fg="gold",bg="black",font=self.default_font)
        self.x19_label.place(x=50,y=780)
        self.entry19=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry19.place(x=100,y=785)


        self.x20_label= Label(self.frame,text="x20",fg="gold",bg="black",font=self.default_font)
        self.x20_label.place(x=50,y=820)
        self.entry20=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry20.place(x=100,y=825)


        self.x21_label= Label(self.frame,text="x21",fg="gold",bg="black",font=self.default_font)
        self.x21_label.place(x=50,y=860)
        self.entry21=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry21.place(x=100,y=865)


        self.x22_label= Label(self.frame,text="x22",fg="gold",bg="black",font=self.default_font)
        self.x22_label.place(x=50,y=900)
        self.entry22=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry22.place(x=100,y=905)


        self.x23_label= Label(self.frame,text="x23",fg="gold",bg="black",font=self.default_font)
        self.x23_label.place(x=50,y=940)
        self.entry23=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry23.place(x=100,y=945)


        self.x24_label= Label(self.frame,text="x24",fg="gold",bg="black",font=self.default_font)
        self.x24_label.place(x=50,y=980)
        self.entry24=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry24.place(x=100,y=985)


        self.x25_label= Label(self.frame,text="x25",fg="gold",bg="black",font=self.default_font)
        self.x25_label.place(x=50,y=1020)
        self.entry25=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry25.place(x=100,y=1025)


        self.x26_label= Label(self.frame,text="x26",fg="gold",bg="black",font=self.default_font)
        self.x26_label.place(x=50,y=1060)
        self.entry26=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry26.place(x=100,y=1065)


        self.x27_label= Label(self.frame,text="x27",fg="gold",bg="black",font=self.default_font)
        self.x27_label.place(x=50,y=1100)
        self.entry27=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry27.place(x=100,y=1105)


        self.x28_label= Label(self.frame,text="x28",fg="gold",bg="black",font=self.default_font)
        self.x28_label.place(x=50,y=1140)
        self.entry28=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry28.place(x=100,y=1145)


        self.x29_label= Label(self.frame,text="x29",fg="gold",bg="black",font=self.default_font)
        self.x29_label.place(x=50,y=1180)
        self.entry29=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry29.place(x=100,y=1185)


        self.x30_label= Label(self.frame,text="x30",fg="gold",bg="black",font=self.default_font)
        self.x30_label.place(x=50,y=1220)
        self.entry30=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry30.place(x=100,y=1225)


        self.x31_label= Label(self.frame,text="x31",fg="gold",bg="black",font=self.default_font)
        self.x31_label.place(x=50,y=1260)
        self.entry31=Text(self.frame,width=25,height=1,font=self.default_font)
        self.entry31.place(x=100,y=1265)

        ################# Put the frame in canvas ####################
        self.canvas.create_window(0, 0, anchor='nw', window=self.frame)
        self.canvas.update_idletasks()

        self.canvas.configure(scrollregion=self.canvas.bbox('all'),yscrollcommand=self.scroll_y.set)

        self.canvas.pack(fill='both', expand=True, side='left')
        self.scroll_y.pack(fill='y', side='right')
    def set_values(self):
        self.entry0.configure(state='normal')
        self.entry0.insert(1.0,"0x00000000")
        self.entry0.configure(state='disabled')


        self.entry1.configure(state='normal')
        self.entry1.insert(1.0,"0x00000000")
        self.entry1.configure(state='disabled')


        self.entry2.configure(state='normal')
        self.entry2.insert(1.0,"0x7FFFFFF0")
        self.entry2.configure(state='disabled')


        self.entry3.configure(state='normal')
        self.entry3.insert(1.0,"0x10000000")
        self.entry3.configure(state='disabled')


        self.entry4.configure(state='normal')
        self.entry4.insert(1.0,"0x00000000")
        self.entry4.configure(state='disabled')


        self.entry5.configure(state='normal')
        self.entry5.insert(1.0,"0x00000000")
        self.entry5.configure(state='disabled')


        self.entry6.configure(state='normal')
        self.entry6.insert(1.0,"0x00000000")
        self.entry6.configure(state='disabled')


        self.entry7.configure(state='normal')
        self.entry7.insert(1.0,"0x00000000")
        self.entry7.configure(state='disabled')


        self.entry8.configure(state='normal')
        self.entry8.insert(1.0,"0x00000000")
        self.entry8.configure(state='disabled')


        self.entry9.configure(state='normal')
        self.entry9.insert(1.0,"0x00000000")
        self.entry9.configure(state='disabled')


        self.entry10.configure(state='normal')
        self.entry10.insert(1.0,"0x00000000")
        self.entry10.configure(state='disabled')


        self.entry11.configure(state='normal')
        self.entry11.insert(1.0,"0x00000000")
        self.entry11.configure(state='disabled')


        self.entry12.configure(state='normal')
        self.entry12.insert(1.0,"0x00000000")
        self.entry12.configure(state='disabled')


        self.entry13.configure(state='normal')
        self.entry13.insert(1.0,"0x00000000")
        self.entry13.configure(state='disabled')


        self.entry14.configure(state='normal')
        self.entry14.insert(1.0,"0x00000000")
        self.entry14.configure(state='disabled')


        self.entry15.configure(state='normal')
        self.entry15.insert(1.0,"0x00000000")
        self.entry15.configure(state='disabled')


        self.entry16.configure(state='normal')
        self.entry16.insert(1.0,"0x00000000")
        self.entry16.configure(state='disabled')


        self.entry17.configure(state='normal')
        self.entry17.insert(1.0,"0x00000000")
        self.entry17.configure(state='disabled')


        self.entry18.configure(state='normal')
        self.entry18.insert(1.0,"0x00000000")
        self.entry18.configure(state='disabled')


        self.entry19.configure(state='normal')
        self.entry19.insert(1.0,"0x00000000")
        self.entry19.configure(state='disabled')


        self.entry20.configure(state='normal')
        self.entry20.insert(1.0,"0x00000000")
        self.entry20.configure(state='disabled')


        self.entry21.configure(state='normal')
        self.entry21.insert(1.0,"0x00000000")
        self.entry21.configure(state='disabled')


        self.entry22.configure(state='normal')
        self.entry22.insert(1.0,"0x00000000")
        self.entry22.configure(state='disabled')


        self.entry23.configure(state='normal')
        self.entry23.insert(1.0,"0x00000000")
        self.entry23.configure(state='disabled')


        self.entry24.configure(state='normal')
        self.entry24.insert(1.0,"0x00000000")
        self.entry24.configure(state='disabled')


        self.entry25.configure(state='normal')
        self.entry25.insert(1.0,"0x00000000")
        self.entry25.configure(state='disabled')


        self.entry26.configure(state='normal')
        self.entry26.insert(1.0,"0x00000000")
        self.entry26.configure(state='disabled')


        self.entry27.configure(state='normal')
        self.entry27.insert(1.0,"0x00000000")
        self.entry27.configure(state='disabled')


        self.entry28.configure(state='normal')
        self.entry28.insert(1.0,"0x00000000")
        self.entry28.configure(state='disabled')


        self.entry29.configure(state='normal')
        self.entry29.insert(1.0,"0x00000000")
        self.entry29.configure(state='disabled')


        self.entry30.configure(state='normal')
        self.entry30.insert(1.0,"0x00000000")
        self.entry30.configure(state='disabled')


        self.entry31.configure(state='normal')
        self.entry31.insert(1.0,"0x00000000")
        self.entry31.configure(state='disabled')
    def change1(self,value):
    	self.entry1.configure(state='normal')
    	self.entry1.delete(1.0,END)
    	self.entry1.insert(1.0,value)
    	self.entry1.configure(state='disabled')
    def change2(self,value):
    	self.entry2.configure(state='normal')
    	self.entry2.delete(1.0,END)
    	self.entry2.insert(1.0,value)
    	self.entry2.configure(state='disabled')
    def change3(self,value):
    	self.entry3.configure(state='normal')
    	self.entry3.delete(1.0,END)
    	self.entry3.insert(1.0,value)
    	self.entry3.configure(state='disabled')
    def change4(self,value):
    	self.entry4.configure(state='normal')
    	self.entry4.delete(1.0,END)
    	self.entry4.insert(1.0,value)
    	self.entry4.configure(state='disabled')
    def change5(self,value):
    	self.entry5.configure(state='normal')
    	self.entry5.delete(1.0,END)
    	self.entry5.insert(1.0,value)
    	self.entry5.configure(state='disabled')
    def change6(self,value):
    	self.entry6.configure(state='normal')
    	self.entry6.delete(1.0,END)
    	self.entry6.insert(1.0,value)
    	self.entry6.configure(state='disabled')
    def change7(self,value):
    	self.entry7.configure(state='normal')
    	self.entry7.delete(1.0,END)
    	self.entry7.insert(1.0,value)
    	self.entry7.configure(state='disabled')
    def change8(self,value):
    	self.entry8.configure(state='normal')
    	self.entry8.delete(1.0,END)
    	self.entry8.insert(1.0,value)
    	self.entry8.configure(state='disabled')
    def change9(self,value):
    	self.entry9.configure(state='normal')
    	self.entry9.delete(1.0,END)
    	self.entry9.insert(1.0,value)
    	self.entry9.configure(state='disabled')
    def change10(self,value):
    	self.entry10.configure(state='normal')
    	self.entry10.delete(1.0,END)
    	self.entry10.insert(1.0,value)
    	self.entry10.configure(state='disabled')
    def change11(self,value):
    	self.entry11.configure(state='normal')
    	self.entry11.delete(1.0,END)
    	self.entry11.insert(1.0,value)
    	self.entry11.configure(state='disabled')
    def change12(self,value):
    	self.entry12.configure(state='normal')
    	self.entry12.delete(1.0,END)
    	self.entry12.insert(1.0,value)
    	self.entry12.configure(state='disabled')
    def change13(self,value):
    	self.entry13.configure(state='normal')
    	self.entry13.delete(1.0,END)
    	self.entry13.insert(1.0,value)
    	self.entry13.configure(state='disabled')
    def change14(self,value):
    	self.entry14.configure(state='normal')
    	self.entry14.delete(1.0,END)
    	self.entry14.insert(1.0,value)
    	self.entry14.configure(state='disabled')
    def change15(self,value):
    	self.entry15.configure(state='normal')
    	self.entry15.delete(1.0,END)
    	self.entry15.insert(1.0,value)
    	self.entry15.configure(state='disabled')
    def change16(self,value):
    	self.entry16.configure(state='normal')
    	self.entry16.delete(1.0,END)
    	self.entry16.insert(1.0,value)
    	self.entry16.configure(state='disabled')
    def change17(self,value):
    	self.entry17.configure(state='normal')
    	self.entry17.delete(1.0,END)
    	self.entry17.insert(1.0,value)
    	self.entry17.configure(state='disabled')
    def change18(self,value):
    	self.entry18.configure(state='normal')
    	self.entry18.delete(1.0,END)
    	self.entry18.insert(1.0,value)
    	self.entry18.configure(state='disabled')
    def change19(self,value):
    	self.entry19.configure(state='normal')
    	self.entry19.delete(1.0,END)
    	self.entry19.insert(1.0,value)
    	self.entry19.configure(state='disabled')
    def change20(self,value):
    	self.entry20.configure(state='normal')
    	self.entry20.delete(1.0,END)
    	self.entry20.insert(1.0,value)
    	self.entry20.configure(state='disabled')
    def change21(self,value):
    	self.entry21.configure(state='normal')
    	self.entry21.delete(1.0,END)
    	self.entry21.insert(1.0,value)
    	self.entry21.configure(state='disabled')
    def change22(self,value):
    	self.entry22.configure(state='normal')
    	self.entry22.delete(1.0,END)
    	self.entry22.insert(1.0,value)
    	self.entry22.configure(state='disabled')
    def change23(self,value):
    	self.entry23.configure(state='normal')
    	self.entry23.delete(1.0,END)
    	self.entry23.insert(1.0,value)
    	self.entry23.configure(state='disabled')
    def change24(self,value):
    	self.entry24.configure(state='normal')
    	self.entry24.delete(1.0,END)
    	self.entry24.insert(1.0,value)
    	self.entry24.configure(state='disabled')
    def change25(self,value):
    	self.entry25.configure(state='normal')
    	self.entry25.delete(1.0,END)
    	self.entry25.insert(1.0,value)
    	self.entry25.configure(state='disabled')
    def change26(self,value):
    	self.entry26.configure(state='normal')
    	self.entry26.delete(1.0,END)
    	self.entry26.insert(1.0,value)
    	self.entry26.configure(state='disabled')
    def change27(self,value):
    	self.entry27.configure(state='normal')
    	self.entry27.delete(1.0,END)
    	self.entry27.insert(1.0,value)
    	self.entry27.configure(state='disabled')
    def change28(self,value):
    	self.entry28.configure(state='normal')
    	self.entry28.delete(1.0,END)
    	self.entry28.insert(1.0,value)
    	self.entry28.configure(state='disabled')
    def change29(self,value):
    	self.entry29.configure(state='normal')
    	self.entry29.delete(1.0,END)
    	self.entry29.insert(1.0,value)
    	self.entry29.configure(state='disabled')
    def change30(self,value):
    	self.entry30.configure(state='normal')
    	self.entry30.delete(1.0,END)
    	self.entry30.insert(1.0,value)
    	self.entry30.configure(state='disabled')
    def change31(self,value):
        self.entry31.configure(state='normal')
        self.entry31.delete(1.0,END)
        self.entry31.insert(1.0,value)
        self.entry31.configure(state='disabled')

# Older root
root=Tk()
gui=GUI(root)
gui.set_values()
root.after(5000,lambda:root.destroy()) # closes after 5000 ms
root.mainloop()
# Updated root
root=Tk() # starting new root
gui=GUI(root)
gui.set_values()
def change_values(rs,value):
    if(value<0):
        value=2**32+value
    value=hex(value)
    value='0x'+value[2:].zfill(8).upper()
    if(rs==0):
    	gui.change0(value)
    elif(rs==1):
    	gui.change1(value)
    elif(rs==2):
    	gui.change2(value)
    elif(rs==3):
    	gui.change3(value)
    elif(rs==4):
    	gui.change4(value)
    elif(rs==5):
    	gui.change5(value)
    elif(rs==6):
    	gui.change6(value)
    elif(rs==7):
    	gui.change7(value)
    elif(rs==8):
    	gui.change8(value)
    elif(rs==9):
    	gui.change9(value)
    elif(rs==10):
    	gui.change10(value)
    elif(rs==11):
    	gui.change11(value)
    elif(rs==12):
    	gui.change12(value)
    elif(rs==13):
    	gui.change13(value)
    elif(rs==14):
    	gui.change14(value)
    elif(rs==15):
    	gui.change15(value)
    elif(rs==16):
    	gui.change16(value)
    elif(rs==17):
    	gui.change17(value)
    elif(rs==18):
    	gui.change18(value)
    elif(rs==19):
    	gui.change19(value)
    elif(rs==20):
    	gui.change20(value)
    elif(rs==21):
    	gui.change21(value)
    elif(rs==22):
    	gui.change22(value)
    elif(rs==23):
    	gui.change23(value)
    elif(rs==24):
    	gui.change24(value)
    elif(rs==25):
    	gui.change25(value)
    elif(rs==26):
    	gui.change26(value)
    elif(rs==27):
    	gui.change27(value)
    elif(rs==28):
    	gui.change28(value)
    elif(rs==29):
    	gui.change29(value)
    elif(rs==30):
    	gui.change30(value)
    elif(rs==31):
    	gui.change31(value)

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
        self.sp =0x7ffffff0
        self.gp= 0x10000000
        self.PC = 0
        self.instruction = 0

    #  storing the instruction in the memory file
    def storeInstruction(self,machine_code):
        self.Register.flush()
        self.Memory.flush()
        self.PC = 0
        self.cycle = 0
        self.Register.update("00010", self.sp)
        self.Register.update("00011",self.gp)

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
            change_values(int(address,2), value)

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
    root.mainloop()
