'''
Created on Aug 2, 2018

@author: yiz
'''

from com.mygui.initStat_func import _get_initstat_session
import datetime
from com.config.config import initStat_configs
import threading
import copy
import uuid
from com.config.config import play_configs, gem_configs
from lxml import etree
from random import randint

picker_cells = ["L0C0R0", "L0C1R0", "L0C2R0", "L0C3R0", "L0C4R0", "L0C5R0", "L0C6R0", "L0C7R0", "L0C8R0", "L0C9R0"]
picker_cell_idx = randint(0, 9)

def __fetchPickerCell():
    global picker_cells
    global picker_cell_idx
    cellName = picker_cells[picker_cell_idx]
    picker_cell_idx += 1
    if picker_cell_idx > 9:
        picker_cell_idx = 0
    return cellName

def _play_thread(_timePerThread, session, tid, url, querystring, payload, payload_picker, header, picker):
    for idx in range(0, _timePerThread):
        payload1 = payload.replace("{tid}", tid)
        picker_rpl = payload_picker.replace("{picker_name}", picker[idx])        
        payload2 = payload1.replace("{picker_repl}", picker_rpl)
        response = session.request("POST", url, data=payload2, headers=header, params=querystring, verify=False)
        node = etree.fromstring(response.text)
        tid = node.xpath("//TransactionId/text()")[0]                

def _measure_mt(timesPerThread, threadNum):
    
    d1 = datetime.datetime.now()
    
    sessions = []
    tids = []
    urls = []
    querys = []
    payloads = []
    payloads_picker = []
    headers = []
    pickers = []
    
    uuid_v = str(uuid.uuid1())
    
    for index in range(0, threadNum):   
        session, tid, nextStage, resp = _get_initstat_session(False, uniqueid = uuid_v + "_" + str(index))
        sessions.append(session)
        tids.append(tid)
        picker = []
        for idx in range(0, timesPerThread):
            name = __fetchPickerCell()
            picker.append(name)
        pickers.append(picker)
        urls.append(copy.deepcopy(play_configs.url))
        querys.append(copy.deepcopy(play_configs.querystring))
        payloads.append(copy.deepcopy(play_configs.payload))
        payloads_picker.append(copy.deepcopy(play_configs.payload_picker['payload']))
        headers.append(copy.deepcopy(play_configs.headers))
        
    #d2 = datetime.datetime.now()
       
    #print( "init state time:" + str( (d2-d1).seconds ) )        
    
    threads = []
    
    for index in range(0, threadNum):
        session = sessions[index]
        tid = tids[index]
        url = urls[index]
        querystring = querys[index]
        payload = payloads[index]
        payload_picker = payloads_picker[index]
        header = headers[index]
        picker = pickers[index]
        uniqueid = uuid_v + "_" + str(index)
        
        querystring.uniqueid = uniqueid
        
        th = threading.Thread(target=_play_thread, args=(timesPerThread, session, tid, url, querystring, payload, payload_picker, header, picker))
        th.start()
        threads.append(th)
    
    for th in threads:
        th.join()
       
    d3 = datetime.datetime.now()
    print( "play time:" + str( (d3-d1).seconds ) )    
            
if __name__ == "__main__":
    _measure_mt(500, 1)
