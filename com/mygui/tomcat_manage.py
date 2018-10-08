'''
Created on Jul 26, 2018

@author: yiz
'''
import os
from subprocess import Popen, PIPE
from com.config.config_global import global_conf
from com.mygui.NonBlockingStreamReader import NonBlockingStreamReader
import psutil
import shutil
import time
import threading

def tomcat_start():
    origPath = os.getcwd()
    try:
        os.chdir(global_conf.tomcat + "\\" + "bin\\")
        proc = Popen(global_conf.tomcat_start, 
          cwd=global_conf.tomcat + "\\" + "bin\\",
          stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
        nbsr = NonBlockingStreamReader(proc.stdout)
        time.sleep(0.5)
        while True:
            output = nbsr.readline(10)
            if not output:
                print('[No more data]')
                break
            print(output)
    except Exception as e:
        print(e.getMessage())
    finally:
        os.chdir(origPath)        

def tomcat_stop():
    origPath = os.getcwd()
    try:
        os.chdir(global_conf.tomcat + "\\" + "bin\\")
        proc = Popen(global_conf.tomcat_stop, 
          cwd=global_conf.tomcat + "\\" + "bin\\",
          stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
        nbsr = NonBlockingStreamReader(proc.stdout)
        time.sleep(0.5)
        while True:
            output = nbsr.readline(5)
            if not output:
                print('[No more data]')
                break
            print(output)
    except Exception as e:
        print(e.getMessage())
    finally:
        os.chdir(origPath)
        
    pids = psutil.pids()
    for pid in pids:
        proc = psutil.Process(pid)
        if proc.name() == "java.exe":
            for cmd in proc.cmdline():
                if cmd.find(global_conf.tomcat) != -1:
                    proc.terminate()
                    break;
            

def tomcat_running():
    pids = psutil.pids()
    for pid in pids:
        proc = psutil.Process(pid)
        if proc.name() == "java.exe":
            for cmd in proc.cmdline():
                if cmd.find(global_conf.tomcat) != -1:
                    return True
    return False            

def _tomcat_deploy():
    if os.path.exists(global_conf.tomcat + "\\webapps\\rgslite"):
        shutil.rmtree(global_conf.tomcat + "\\webapps\\rgslite")
    shutil.copytree(global_conf.ant_build_social + "..\\build\\target\\tomcat\\domains\\rgs\\webapps\\rgslite", global_conf.tomcat + "\\webapps\\rgslite")

def _tomcat_deplay_wrapper(progBar, root):
    try:        
        t = threading.Thread(target=_tomcat_deploy)
        t.start()
        while True:
            t.join(0.1)
            if t.isAlive():
                progBar.step(5)
                progBar.update_idletasks()
                root.update_idletasks()
            else:
                progBar["value"]=100
                progBar.update_idletasks()
                break;
    except:
        print("tomcat_deploy_wrapper failed!")    

def tomcat_deploy(progBar, root):
    try:
        t = threading.Thread(target=_tomcat_deplay_wrapper, args=(progBar, root))
        t.start()
    except:
        print("tomcat_deploy failed!")
                
if __name__ == "__main__":
    tomcat_stop()