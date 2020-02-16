import subprocess
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

