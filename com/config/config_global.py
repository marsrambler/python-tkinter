'''
Created on Jul 26, 2018

@author: yiz
'''
from com.config.config_core import toDict
from random import randint

_global_conf = {
            'storage': 'c:\\rgs_ _workFlow',
            
#             'prot': 'http',
#             'ip': '127.0.0.1',
#             'port': '8980',
#             'webapp': '/ ',
                        
#             'prot': 'https',
#             'ip': '127.0.0.1',
#             'port': '6443',
#             'webapp': '',
            
            'prot': 'http',
            'ip': ' ',
            'port': '37042',
            'webapp': '/ ',
            
            'use_proxy': False,                        
            'softwareId': '200 ',            
            'uniqueid' : 'F001- 7',
            'BetPerPattern': '1',
            'PatternsBet': '75',
            'browser': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s',
            'ant_path': 'C:\\ \\tools\\apache-ant-1.9.2\\bin\\ant.bat',
            'tomcat': 'C:\\green-install\\tomcat-RGSserver-7.0.78-3\\', 
            #'tomcat- -workable\\',
            'tomcat_start': 'startup.bat',
            'tomcat_stop': 'shutdown.bat',
            'ant_build_dir': 'D:\\ \\build\\',
            'ant_build_social': 'D:\\ \\ \\',
            'paytable_dir': ' ',
            'histo_ids': ["200- -001"],
            'histo_times': '100000000',
            'histo_cpus': '10'
        }

_picker_conf = {
            'pickerStages':
            [
            {
             'stageName': 'FreeSpinPicker',
             'cells': ["L0C0R0", "L0C1R0", "L0C2R0", "L0C3R0", "L0C4R0"],
             'start_idx': randint(0, 4)
            }, 
            {
             'stageName': 'MlpPicker',
             'cells': ["L0C0R0", "L0C1R0", "L0C2R0", "L0C3R0", "L0C4R0", "L0C5R0", "L0C6R0", "L0C7R0", "L0C8R0", "L0C9R0", "L0C10R0", "L0C11R0"],
             'start_idx': randint(0, 11)             
            }
            ]
        }

global_conf = toDict(_global_conf)
picker_conf = toDict(_picker_conf)

if __name__ == "__main__":
    print(picker_conf)
