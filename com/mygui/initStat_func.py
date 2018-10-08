'''
Created on Jul 24, 2018

@author: yiz
'''
import sys
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xml.dom import minidom
from logging import raiseExceptions
from lxml import etree
from com.config.config import initStat_configs, gem_configs
from com.mygui.LXmlParser import XMLFileParser
import os
from tkinter import messagebox

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def _get_initstat_session(printLog=False, **kw):
    url = initStat_configs.url
    querystring = initStat_configs.querystring
    if kw is not None:
        for key in kw.keys():
            if querystring[key] is not None:
                querystring[key] = kw[key]
    headers = initStat_configs.headers
    req_session = requests.Session()
    try:
        if printLog:
            print("init stat:")
            print("url: {}".format(url))
            print("params: {}".format(querystring))
        response = req_session.request("GET", url, headers=headers, params=querystring, verify=False)
        if printLog:
            print("response:")
            print(response.text)    
        node  = etree.fromstring(response.text)
        trans = node.xpath("//TransactionId/text()")
        if trans is None or len(trans) == 0:
            raise Exception(response.text[0:100])
        sub_text2 = trans[0]
        nextStage = node.xpath("//NextStage/text()")[0]
        return req_session, sub_text2, nextStage, response.text
    except Exception as e:
        msg = '{0}'.format(e)
        messagebox.showinfo("ERROR", msg)
        raise e

def initStat_func():
    session, tid, nextStage, resp_text = _get_initstat_session(True)
    fileName = gem_configs.origStore + "\\" + "initStat" + "_" + tid + ".xml"
    while os.path.exists(fileName):
        tmpname = fileName[0:-4]
        fileName = tmpname + "_copy" + ".xml"
    parser = XMLFileParser(resp_text, fileName)
    return session, tid, nextStage, parser