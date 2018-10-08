'''
Created on Jul 26, 2018

@author: yiz
'''
import sys
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xml.dom import minidom
from logging import raiseExceptions
from lxml import etree
from com.config.config import initStat_configs, gem_configs, paytable_configs
from com.mygui.LXmlParser import XMLFileParser
import os
from tkinter import messagebox

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def _get_paytable_session(printLog=False):
    url = paytable_configs.url
    querystring = paytable_configs.querystring
    headers = paytable_configs.headers
    
    try:
        if printLog:
            print("get paytable:")
            print("url: {}".format(url))
            print("params: {}".format(querystring))    
        response = requests.request("GET", url, headers=headers, params=querystring, verify=False)
        if printLog:
            print("response:")
            print(response.text)      
        return response.text 
    except Exception as e:
        msg = '{0}'.format(e)
        messagebox.showinfo("ERROR", msg)
        raise e        

def getPayTable_func():
    resp_text = _get_paytable_session(True)
    fileName = gem_configs.origStore + "\\" + "getPaytable" + "_"  + ".xml"
    while os.path.exists(fileName):
        tmpname = fileName[0:-4]
        fileName = tmpname + "_copy" + ".xml"
    parser = XMLFileParser(resp_text, fileName)
    return parser