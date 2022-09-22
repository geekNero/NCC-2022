import subprocess
import os
os.chdir('src')
er=open('error.txt','w+')
rc=open('return_code.txt','w+')
def func(language):
    if(language=="python"):
        py()
    elif(language=="c++"):
        cpp()
    elif(language=="c"):
        c()
def py():
    a=subprocess.run('python3 code.py <input.txt>output.txt',shell=True,stderr=er,text=True)
    rc.write(str(a.returncode))
    rc.close()
    er.close()
def cpp():
    a=subprocess.run('g++ code.cpp -o cpp.out',shell=True,stderr=er,text=True)
    rc.write(str(a.returncode))
    if(a.returncode==0):
        a=subprocess.run('./cpp.out <input.txt>output.txt',shell=True,stderr=er,text=True)
        rc.write(str(a.returncode))
    rc.close()
    er.close()

def c():
    a=subprocess.run('gcc code.c -o c.out',shell=True,stderr=er,text=True)
    rc.write(str(a.returncode))
    if(a.returncode==0):
        a=subprocess.run('./c.out <input.txt>output.txt',shell=True,stderr=er,text=True)
        rc.write(str(a.returncode))
    rc.close()
    er.close()

cpp()