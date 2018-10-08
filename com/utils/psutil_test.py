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
        proc_name1.append(proc.name())
    proc_name1.sort()
    print(proc_name1)
    
    tomcat_start()
    
    proc_name2 = []
    
    pids = psutil.pids()
    for pid in pids:
        proc = psutil.Process(pid) 
        proc_name2.append(proc.name())
    proc_name2.sort()
    print(proc_name2)
    
    proc_name3 = list(set(proc_name2) - set(proc_name1))
    print("difference:") 
    print(proc_name3)   