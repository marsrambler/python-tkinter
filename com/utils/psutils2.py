'''
Created on Jul 30, 2018

@author: yiz
'''
import psutil
from com.mygui.tomcat_manage import tomcat_start

if __name__ == "__main__":
    
    proc_name1 = []
    pids = psutil.pids()
    for pid in pids:
        proc = psutil.Process(pid) 
        if proc.name() == "java.exe":
            print(proc.exe())
            print(proc.cmdline())
            #print(proc.terminate())
            #out = proc.terminal()
            #print(type(out))