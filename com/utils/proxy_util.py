'''
Created on Aug 23, 2018

@author: yiz
'''

import winreg
import os

env_http_proxy  = None
env_https_proxy = None
env_no_proxy = None

ie_key  = None
ie_type = None

INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_ALL_ACCESS)

def enable_ie_proxy():
    _key, _type = winreg.QueryValueEx(INTERNET_SETTINGS, 'ProxyEnable')
    winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, _type, 1)
    
    global ie_key
    global ie_type
    winreg.SetValueEx(INTERNET_SETTINGS, 'AutoConfigURL', 0, ie_type, ie_key) 

def disable_ie_proxy():
    global ie_key
    global ie_type    
    ie_key, ie_type = winreg.QueryValueEx(INTERNET_SETTINGS, 'AutoConfigURL')
    #winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, _type, 0)    
    
    _key, _type = winreg.QueryValueEx(INTERNET_SETTINGS, 'ProxyEnable')
    winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, _type, 0)

    
        

def enable_proxy_in_env_var():
    pass;

def disable_proxy_in_env_var():
    for key in os.environ.keys():
        if key == "HTTP_PROXY":
            env_http_proxy = os.environ.get("HTTP_PROXY", "")
            os.environ.pop("HTTP_PROXY")
        elif key == "HTTPS_PROXY":
            env_https_proxy = os.environ.get("HTTPS_PROXY", "")
            os.environ.pop("HTTPS_PROXY")
        elif key == "NO_PROXY":
            env_no_proxy = os.environ.get("NO_PROXY", "")
            os.environ.pop("NO_PROXY")
            
if __name__ == "__main__":
    print("1: " + os.environ.get("HTTP_PROXY", ""))
    print("2: " + os.environ.get("HTTPS_PROXY", ""))
    print("3: " + os.environ.get("NO_PROXY", ""))
    disable_proxy_in_env_var()
    print("1: " + os.environ.get("HTTP_PROXY", ""))
    print("2: " + os.environ.get("HTTPS_PROXY", ""))
    print("3: " + os.environ.get("NO_PROXY", ""))    
    