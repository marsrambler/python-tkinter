'''
Created on Aug 8, 2018

@author: yiz
'''

import copy
import uuid
from random import randint

distr_histo = {
               'software_id': '200-1468-001',
               'pattensBet': '75',
               'servers':
               [
#                 {
#                     'id': '0',
#                     'uniqueId_postfix': str(uuid.uuid1()),
#                     'server_ip': ' ',
#                     'initStat_url': ' ',
#                     'play_url': ' ',
#                     'thread_num': '10',
#                     'tasksPerThread': '10',
#                     'spinsPerTask': '50'
#                 },
#                 {
#                     'id': '1',
#                     #'uniqueId_postfix': str(uuid.uuid1()),
#                     'uniqueId_postfix': '_histo_6',
#                     'server_ip': ' ',
#                     'initStat_url': ' ',
#                     'play_url': ' ',
#                     'thread_num': '1',
#                     'tasksPerThread': '100',
#                     'spinsPerTask': '10',
#                     'maxPickerTimes': '20',
#                     'play_id': [
#                                 [
#                                 0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #50
#                                 0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #100
#                                 0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #150
#                                 0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #200
#                                 0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #250
#                                 0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #300                                                                                                                                                                                                                                                                                                                                                                       
#                                 ],
#                             ]                                      
#                 },
                {
                    'id': '2',
                    #'uniqueId_postfix': str(uuid.uuid1()),
                    'uniqueId_postfix': '_histo_6',
                    'server_ip': '127.0.0.1',
                    'initStat_url': 'http://127.0.0.1:8980/ /tc/initstate',
                    'play_url': 'http://127.0.0.1:8980/ /tc/play',
                    'thread_num': '1',
                    'tasksPerThread': '10',
                    'spinsPerTask': '1000',
                    'maxPickerTimes': '20',
                    'play_id': [
                                [
                                0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #50
                                0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #100
                                0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #150
                                0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #200
                                0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #250
                                0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  0,0,0,0,0,  #300                                                                                                                                                                                                                                                                                                                                                                       
                                ],
                            ]                
                }                
               ],
               
               'pickerStages':
               [
                    {
                     'stageName': 'FreeSpinPicker',
                     'cells': ["L0C0R0", "L0C1R0", "L0C2R0", "L0C3R0", "L0C4R0"],
                     'start_idx': randint(0, 4),
                     'strategy': 'random',
                     'maxRandom': 4
                    }, 
                    {
                     'stageName': 'MlpPicker',
                     'cells': ["L0C0R0", "L0C1R0", "L0C2R0", "L0C3R0", "L0C4R0", "L0C5R0", "L0C6R0", "L0C7R0", "L0C8R0", "L0C9R0", "L0C10R0", "L0C11R0"],
                     'start_idx': randint(0, 11),
                     'strategy': 'default'             
                    }
               ]               
            }
# output:
# dict, uniqueId
# {
#    'server_ip' : uniqueId[thread_num][tasksPerThread]
# }

def generateUniqueId():
    global distr_histo
    uniqueIdMap = dict()
    
    for server in distr_histo['servers']:
        uniqueIdPerThread = []
        for id_thread in range(0, int(server['thread_num'])):
            uniqueIdPerTask = []
            for id_task in range(0, int(server['tasksPerThread'])):
                uniqueId = server['id'] + "_th-" + str(id_thread) + "_tk-" + str(id_task) + "_" + server['uniqueId_postfix']
                uniqueIdPerTask.append(uniqueId)
            uniqueIdPerThread.append(uniqueIdPerTask)
        uniqueIdMap[server['server_ip']] = uniqueIdPerThread
        
    return uniqueIdMap

initStat_querystring = {"":"",
                        "showInitialCashier":"false","parametersFromConfigCall":"true","nscashout":"","defaultbuyinamount":"1000.0",
                        "softwareid":'{??}',"language":"en","countrycode":"US","istournament":"false","nscode":"DDI",
                        "game":"CrystalSlipper","audio":"on","skincode":"DDI-SKIN1","minbet":"333","ipaddress":'{??}',"moduleAssetPath":"/gpe",
                        "affiliate":"","uniqueid":'{??}',"time":"1499076423173"}

# output:
# dict, querystring
# {
#    'server_ip' : querystring[thread_num][tasksPerThread]
# }

def generateInitStatQueryString(_uniqueIdMap):
    global distr_histo
    global initStat_querystring
    initStat_querystring_Map = dict()
   
    for server in distr_histo['servers']:
        is_qs_per_thread = []
        for id_thread in range(0, int(server['thread_num'])):
            is_qs_per_task = []
            for id_task in range(0, int(server['tasksPerThread'])):
                qs = copy.deepcopy(initStat_querystring)
                qs['softwareid'] = distr_histo['software_id']
                qs['ipaddress']  = server['server_ip']
                qs['uniqueid']   = _uniqueIdMap[ server['server_ip'] ][id_thread][id_task]
                is_qs_per_task.append(qs)
            is_qs_per_thread.append(is_qs_per_task)
        initStat_querystring_Map[server['server_ip']] = is_qs_per_thread
    
    return initStat_querystring_Map

initStat_headers = {
                    'cache-control': "no-cache",
                    'postman-token': "9bd48c77-8fca-847b-b35a-00f5d7a1b0ec"
                    }

# output:
# dict, uniqueId
# {
#    'server_ip' : header[thread_num][tasksPerThread]
# }

def generateInitStatHeaders():
    global distr_histo
    global initStat_headers
    initStat_header_Map = dict()
   
    for server in distr_histo['servers']:
        is_hd_per_thread = []
        for id_thread in range(0, int(server['thread_num'])):
            is_hd_per_task = []
            for id_task in range(0, int(server['tasksPerThread'])):
                hd = copy.deepcopy(initStat_headers)
                is_hd_per_task.append(hd)
            is_hd_per_thread.append(is_hd_per_task)
        initStat_header_Map[server['server_ip']] = is_hd_per_thread
    
    return initStat_header_Map


play_querystring = {
                    "":"","showInitialCashier":"false","parametersFromConfigCall":"true","nscashout":"","defaultbuyinamount":"1000.0",
                    "softwareid":'{??}',"language":"en","countrycode":"US","istournament":"false","nscode":"DDI","denomid":"3342",
                    "skincode":"DDI-SKIN1","minbet":"333","ipaddress":'{??}',"moduleAssetPath":"/gpe","affiliate":"","uniqueid":'{??}',
                    "time":"1499076461333"
                }

# output:
# dict, uniqueId
# {
#    'server_ip' : querystring[thread_num][tasksPerThread]
# }

def generatePlayQueryString(_uniqueIdMap):
    global distr_histo
    global play_querystring
    play_querystring_Map = dict()
   
    for server in distr_histo['servers']:
        pl_qs_per_thread = []
        for id_thread in range(0, int(server['thread_num'])):
            pl_qs_per_task = []
            for id_task in range(0, int(server['tasksPerThread'])):
                qs = copy.deepcopy(play_querystring)
                qs['softwareid'] = distr_histo['software_id']
                qs['ipaddress']  = server['server_ip']
                qs['uniqueid']   = _uniqueIdMap[ server['server_ip'] ][id_thread][id_task]
                pl_qs_per_task.append(qs)
            pl_qs_per_thread.append(pl_qs_per_task)
        play_querystring_Map[server['server_ip']] = pl_qs_per_thread
    
    return play_querystring_Map

play_payload = {
                'payload' : 
                
                '<GameLogicRequest>\n  \
                    <TransactionId>{tid}</TransactionId>\n  \
                    <PatternSliderInput>\n    \
                        <BetPerPattern>1</BetPerPattern>\n    \
                        <PatternsBet>{patternBet}</PatternsBet>\n  \
                    </PatternSliderInput>\n  \
                    {picker_repl}\n \
                </GameLogicRequest>'
                }

# output:
# dict, uniqueId
# {
#    'server_ip' : payload[thread_num][tasksPerThread]
# }

def generatePayload():
    global distr_histo
    global play_payload
    payload_Map = dict()
   
    for server in distr_histo['servers']:
        payload_per_thread = []
        for id_thread in range(0, int(server['thread_num'])):
            payload_per_task = []
            for id_task in range(0, int(server['tasksPerThread'])):
                pld = copy.deepcopy(play_payload)
                pld1 = pld['payload'].replace("{patternBet}", distr_histo['pattensBet'])
                payload_per_task.append(pld1)
            payload_per_thread.append(payload_per_task)
        payload_Map[server['server_ip']] = payload_per_thread
    
    return payload_Map

play_payload_picker = {
                    'payload':
                    
                    '<PickerInput>\n    \
                        <Pick name=\"{picker_name}\"/>\n  \
                    </PickerInput>'
                }

def _fetchPickerCell(_stage):
    cellName = _stage['cells'][ _stage['start_idx'] ]
    _stage['start_idx'] += 1
    if _stage['start_idx'] >= len(_stage['cells']):
        _stage['start_idx'] = 0
    return cellName

# output:
# dict, pickerName
# {
#    'server_ip' : 
#    {'stageName' :
#     pickerName[thread_num][tasksPerThread][spinsPerTask]
#    }
# }

def _generateStagePickers():
    global distr_histo
    global play_payload_picker
    
    _picker_server_Map = dict()
    for server in distr_histo['servers']:
        pick_per_thread = []
        for id_thread in range(0, int(server['thread_num'])):
            pick_per_task = []
            for id_task in range(0, int(server['tasksPerThread'])):
                pick_per_stage = dict()
                for stage in distr_histo['pickerStages']:
                    _stage_name      = stage['stageName']
                    _stage_cells     = stage['cells']
                    _stage_start_idx = stage['start_idx']
                    pick_per_spin = []
                    for id_spin in range(0, int(server['maxPickerTimes'])):
                        name = _fetchPickerCell(stage)
                        pld_picker  = copy.deepcopy(play_payload_picker)
                        _picker_dst = pld_picker['payload'].replace("{picker_name}", name)
                        pick_per_spin.append(_picker_dst)                        
                    pick_per_stage[_stage_name] = pick_per_spin                     
                pick_per_task.append(pick_per_stage)        
            pick_per_thread.append(pick_per_task)
        _picker_server_Map[server['server_ip']] = pick_per_thread
    return _picker_server_Map


play_headers = {
                'cache-control': "no-cache",
                'postman-token': "b90a76d7-bf05-4dcf-3388-6700aed7e1c1" 
            }

# output:
# dict, uniqueId
# {
#    'server_ip' : uniqueId[thread_num][tasksPerThread]
# }

def generatePlayHeaders():
    global distr_histo
    global play_headers
    play_header_Map = dict()
   
    for server in distr_histo['servers']:
        pl_hd_per_thread = []
        for id_thread in range(0, int(server['thread_num'])):
            pl_hd_per_task = []
            for id_task in range(0, int(server['tasksPerThread'])):
                hd = copy.deepcopy(play_headers)
                pl_hd_per_task.append(hd)
            pl_hd_per_thread.append(pl_hd_per_task)
        play_header_Map[server['server_ip']] = pl_hd_per_thread
    
    return play_header_Map


uniqueIdMap = generateUniqueId()
initStat_querystring = generateInitStatQueryString(uniqueIdMap)
initStat_headers = generateInitStatHeaders()

play_querystring = generatePlayQueryString(uniqueIdMap)
play_load = generatePayload()
play_load_picker = _generateStagePickers()
#play_pickers = generatePickerNames()
play_headers = generatePlayHeaders()


if __name__ == "__main__":
    #unq_Map = generateUniqueId()
    #print(play_load_picker)
    pass