'''
Created on Jul 25, 2018

@author: yiz
'''
import sys
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xml.dom import minidom
from logging import raiseExceptions
from lxml import etree
from com.config.config import play_configs, gem_configs
from com.mygui.LXmlParser import XMLFileParser
import os
from tkinter import messagebox
from com.config.config_global import picker_conf

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def _getPickerCellByStage(cellArray, cellIdx):
    cellName = cellArray[cellIdx]
    cellIdx += 1
    if len(cellArray) == cellIdx:
        cellIdx = 0
    return cellName, cellIdx


def _play_func(session, tid, nextStage=None, printLog=False, **kw):
    url = play_configs.url
    querystring = play_configs.querystring
    if kw is not None:
        for key in kw.keys():
            if querystring[key] is not None:
                querystring[key] = kw[key]
    
    payload = play_configs.payload    
    headers = play_configs.headers
    payload1 = payload.replace("{tid}", tid)
        
    match = False
    for pickerStage in picker_conf.pickerStages:
        if pickerStage['stageName'] == nextStage:
            match = True
            break
    
    if not match:
        payload2 = payload1.replace("{picker_repl}", "")        
    else: 
        payload_picker = play_configs.payload_picker       
        _cellName, _nextIdx = _getPickerCellByStage(pickerStage['cells'], pickerStage['start_idx'])
        _picker = payload_picker.payload.replace("{picker_name}", _cellName)
        payload2 = payload1.replace("{picker_repl}", _picker)        
        pickerStage['start_idx'] = _nextIdx
    
    try:
        if printLog:
            print("play:")
            print("url: {}".format(url))
            print("params: {}".format(querystring))
            print("payload: {}".format(payload2))        
        response = session.request("POST", url, data=payload2, headers=headers, params=querystring, verify=False)
        if printLog:
            print("response:")
            print(response.text)                   
        node  = etree.fromstring(response.text)
        trans = node.xpath("//TransactionId/text()")
        if trans is None or len(trans) == 0:
            raise Exception(response.text[0:100])            
        transId   = trans[0]
        nextStage = node.xpath("//NextStage/text()")[0]             
        return transId, nextStage, response.text
    except Exception as e:
        msg = '{0}'.format(e)
        messagebox.showinfo("ERROR", msg)
        raise e

def play_func(session, _tid, _nextStage=None):
    tid, nextStage, resp_text = _play_func(session, _tid, _nextStage, True)
    fileName = gem_configs.origStore + "\\" + "play" + "_" + tid + ".xml"
    while os.path.exists(fileName):
        tmpname = fileName[0:-4]
        fileName = tmpname + "_copy" + ".xml"
    parser = XMLFileParser(resp_text, fileName)
    return tid, nextStage, parser