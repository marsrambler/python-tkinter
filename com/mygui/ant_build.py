'''
Created on Jul 26, 2018

@author: yiz
'''
import os
import threading
from subprocess import Popen, PIPE
from shutil import copyfile
from com.config.config_global import global_conf
from com.mygui.NonBlockingStreamReader import NonBlockingStreamReader

def _ant_build_social(progBar, root):
    idx = 0;
    origPath = os.getcwd()
    try:
        os.chdir(global_conf.ant_build_social)
        ant_cmd = "ant -f {0} {1} 2>&1".format("./build.xml", "package-lite")
        for line in os.popen(ant_cmd):
            print(line)
            idx += 1
            if idx % 5 == 0:
                progBar.step(5)
                progBar.update_idletasks()
                root.update_idletasks()
        
        os.chdir(global_conf.ant_build_social + "..//token//")
        ant_cmd = "ant -f {0} {1} 2>&1".format("./build.xml", "token-replace")
        for line in os.popen(ant_cmd):
            print(line)        
    except Exception as e:
        print(e.getMessage())
    finally:
        os.chdir(origPath)        
    
    progBar["value"]=100
    progBar.update_idletasks()    
    
def ant_build_social(progBar, root):        
    try:
        t = threading.Thread(target=_ant_build_social, name="ant-build-social", args=(progBar, root))
        t.start()
    except:
        print("Error in start new thread")

def _ant_build_glecomponent(progBar, root):
    idx = 0;
    origPath = os.getcwd()
    try:
        os.chdir(global_conf.ant_build_social+"\\..\\repo_gle_core\\")
        ant_cmd = "ant -f {0} {1} 2>&1".format("./build.xml", "compile")
        for line in os.popen(ant_cmd):
            print(line)
            idx += 1
            if idx % 5 == 0:
                progBar.step(5)
                progBar.update_idletasks()
                root.update_idletasks()
            #if line.find("gle-components-2.0.0.jar") != -1:
            #    break;
        file_src = global_conf.ant_build_dir + "\\GLE\\classes\\gle-components-2.0.0.jar"
        file_dst = global_conf.tomcat + "\\webapps\\rgslite\\WEB-INF\\classes\\gle-components-2.0.0.jar"
        copyfile(file_src, file_dst)
        #os.chdir(global_conf.ant_build_social + "..//token//")
        #ant_cmd = "ant -f {0} {1} 2>&1".format("./build.xml", "token-replace")
        #for line in os.popen(ant_cmd):
        #    print(line)        
    except Exception as e:
        print(e.getMessage())
    finally:
        os.chdir(origPath)        
    
    progBar["value"]=100
    progBar.update_idletasks()    


def ant_build_glecomponent(progBar, root):
    try:
        t = threading.Thread(target=_ant_build_glecomponent, name="ant-build-glecomponent", args=(progBar, root))
        t.start()
    except:
        print("Error in start new thread for glecomponent")
     
if __name__ == "__main__":
    ant_build_social()