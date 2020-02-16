import sys
import subprocess
import os
exec(open("./utility.py").read())
class mycmd(gdb.Command):
    inferiors=  0
    inf_isX86=  0
    inf_isX64=  0
    def __init__(self,chname):
        super(mycmd, self).__init__(chname,gdb.COMMAND_USER)
        self.inferiors = gdb.inferiors()
        if(self.inferiors[0].architecture()=="i386"):
            inf_isX86=True
            inf_isX64=False
        else:
            inc_isX64=True
            inf_isX86=False
    

class pbreak(mycmd):
    filehdl= 0# {{{
    def __init__(self):
        super(pbreak, self).__init__("pbreak")
    def isCPP(self,arg):
        if(arg.find(".c")!=-1 or arg.find(".h")!=-1):
            return True
        else:
            return False
    def isAddress(self,arg):
        try:
            dat= int(arg,16)
        except:
            return False
        return dat>=getLoadAddr(self.inferiors[0])

    def isOffset(self,arg):
        try:
            dat= int(arg,16)
        except:
            return False
        return dat< getLoadAddr(self.inferiors[0])

    def invoke(self, arg, from_tty):
        self.filehdl = open("./.gdb_breakpoints","a+")
        if(arg==''):
            for line in self.filehdl:
                gdb.execute(line[:-1])
            return
        if(self.isCPP(arg)):
            print("isCPP")
            expression="break "+arg
            gdb.execute(expression)
            self.filehdl.write(expression+'\n')
            self.filehdl.flush()
        elif(self.isAddress(arg)):
            print("isADDR")
            expression="break * "+arg
            gdb.execute(expression)
            self.filehdl.write(expression+'\n')
            self.filehdl.flush()
        elif(self.isOffset(arg)):
            print("isOFFSET")
            gdb.execute("piebreak "+arg)
            self.filehdl.write("piebreak "+arg+'\n')
            self.filehdl.flush()
        else:
            return False
# }}}

class showpbp(mycmd):
    def __init__(self):# {{{
        super(showpbp, self).__init__("showpbp")
    def invoke(self, arg, from_tty):
        try:
            self.filehdl = open("./.gdb_breakpoints",'r')
        except:
            print("No persistent breakpoints")
        idx=0
        for line in self.filehdl:
            idx+=1
            print('['+str(idx)+'] '+line[:-1])# }}}

class delpbp(mycmd):
    def __init__(self):
        super(delpbp, self).__init__("delpbp")
    def invoke(self, arg, from_tty):
        pass
        ##怎么解析记录unbreak bps
        
pbreak()
showpbp()
