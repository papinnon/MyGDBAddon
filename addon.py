import sys
import subprocess
import os
import logging as log

# This addons is dedicated to make gdb debugging faster for ctf pwnables

#inferior : The process runs under gdb
#   Inferior class has several attributes corresponding to the proccess info,pid...
#   So, im gonna using inferior class to implement aslr-address detection(/proc/pid/maps)
#   When pwning(attach) an PIE elf, its hard to set breakpoints, so it is worth to create an wrapper for the 'break' command to make gdb break at an PIE offset.

#If we have one_gadget installed, add a command as a wrapper for it. 
#For format string vulnerabilities, add a command to easy develop exploits.
#For 

def getLoadAddr(inferior):
    arch = inferior.architecture()
    modulename = inferior.progspace.filename
    data = subprocess.getoutput("cat /proc/"+str(inferior.pid)+"/maps")
    if(arch.name()=='i386'):
        idx = data.find(modulename) 
        return int(data[idx-73:idx-65],16)
    elif(arch.name()=="i386:x86-64"):
        idx = data.find(modulename)
        return int(data[idx-73:idx-61],16)
    else:
        return False



blist = []
class piebreak(gdb.Command):
    base = 0
    pid=0
    inferior=0
    def __init__(self):
        super(piebreak, self).__init__("piebreak",gdb.COMMAND_USER)
    def dobreak(self):
        global blist
        self.pid = self.inferior.pid
        self.base = getLoadAddr(self.inferior)
        blist = list(dict.fromkeys(blist))
        for i in blist:
            gdb.execute("break *"+hex(self.base+i))
        blist.clear()

    def invoke(self, arg, from_tty):
        global blist
        self.inferior = gdb.inferiors()[0]
        if(arg==''):
            self.dobreak()
            return 
        try:
            offset = int(arg,10)
        except:
            offset = int(arg,16)
        blist.append(offset)
        if(self.inferior.pid == 0):
            return 
        self.dobreak()
        return

class sti(gdb.Command):
    def __init__(self):
        super(sti, self).__init__("sti",gdb.COMMAND_USER)
    def invoke(self,arg,from_tty):
        global blist
        blist = list(dict.fromkeys(blist))
        for i in blist:
            gdb.execute("break *"+hex(base+i))
        gdb.execute("starti")


piebreak()
