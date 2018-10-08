'''
Created on Jul 30, 2018

@author: yiz
'''
import os
import threading
from subprocess import Popen, PIPE
from com.config.config_global import global_conf
import time
import io

def _ant_run_histo(his_times, his_cpus, his_id, progBar, root):
    origPath = os.getcwd()
    try:
        os.chdir(global_conf.paytable_dir)
        proc = Popen(global_conf.ant_path + " histo", 
                      cwd=global_conf.paytable_dir,
                      stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
        stdin_wrapper = io.TextIOWrapper(proc.stdin)
        time.sleep(1)
        
        while True:
            output = proc.stdout.readline()
            if not output:
                print(output)
                print('[No more data]')
                break
            elif output.decode("utf-8").find("Enter Histo Runs") != -1:
                stdin_wrapper.write(his_times + "\r\n")
                stdin_wrapper.flush()
            elif output.decode("utf-8").find("Enter Number of Threads") != -1:
                stdin_wrapper.write(his_cpus + "\r\n")
                stdin_wrapper.flush()
            elif output.decode("utf-8").find("Enter SoftwareId") != -1:
                stdin_wrapper.write(his_id + "\r\n")
                stdin_wrapper.flush()                            
            print(output.decode("utf-8"))
            progBar.step(20)
            progBar.update_idletasks()
            root.update_idletasks()
            
        newName = "histo_result"+"_"+his_id
        while os.path.exists(newName):
            newName += "_copy"
        if os.path.exists("histo_result"):
            os.renames("histo_result", newName)
        
    except Exception as e:
        print(e.getMessage())
    finally:
        os.chdir(origPath)

def _run_histo_wrapper(progBar, root):
    try:
        for s_id in global_conf.histo_ids:
            tr = threading.Thread(target=_ant_run_histo, args=(global_conf.histo_times, global_conf.histo_cpus, s_id, progBar, root))
            tr.start()
            tr.join()
    except:
        print("Error in start thread wrapper")
        
    progBar["value"]=100
    progBar.update_idletasks()     
    
def ant_run_histo(progBar, root):
    try:
        t = threading.Thread(target=_run_histo_wrapper, name="ant-run-histo", args=(progBar, root))
        t.start()
    except:
        print("Error in start new thread")

if __name__ == "__main__":
    ant_run_histo() 