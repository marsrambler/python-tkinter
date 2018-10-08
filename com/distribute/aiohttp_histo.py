'''
Created on Aug 8, 2018

@author: yiz
'''
import aiohttp
import asyncio
from lxml import etree
import threading
import datetime
from random import randint
from com.mygui.LXmlParser import XMLFileParser, XMLFileParserInc
from com.distribute.config.distr_config import distr_histo, initStat_querystring, initStat_headers
from com.distribute.config.distr_config import play_querystring, play_load, play_load_picker, play_headers

class SingleThreadTask():
    
    filter_inc = ["//OutcomeDetail", "//PrizeOutcome", "//GameLogicResponse"]
    
    def __init__(self, _serverId, _taskId):
        self._serverId = _serverId
        self._taskId   = _taskId
    
    def setInitStatParams(self, _url, _querystring, _headers):
        self.url_initStat         = _url
        self.querystring_initStat = _querystring
        self.headers_initStat     = _headers
    
    def setPlayParams(self, _url, _querystring, _payload, _picker, _headers, _play_id_task):
        self.url_play         = _url
        self.querystring_play = _querystring
        self.payload_play     = _payload
        self.picker_play      = _picker        
        self.headers_play     = _headers
        self.play_idx_play    = _play_id_task
        self.stage_idx_play   = 0        
    
    def _isPickerStage(self):
        isPickerStage = False
        for stage in distr_histo['pickerStages']:
            if stage['stageName'] == self.nextStage:
                isPickerStage = True
        return isPickerStage
    
    def _getPickerStrategy(self):
        if not self._isPickerStage():
            return None
        else:
            for stage in distr_histo['pickerStages']:
                if stage['stageName'] == self.nextStage:
                    return stage['strategy']
            return None            

    def _getPickerMaxRandom(self):
        if self._getPickerStrategy() != "random":
            return None
        else:
            for stage in distr_histo['pickerStages']:
                if stage['stageName'] == self.nextStage:
                    return stage['maxRandom']
            return None
        
    def _isPickerStage_curr(self):
        isPickerStage = False
        for stage in distr_histo['pickerStages']:
            if stage['stageName'] == self.currStage:
                isPickerStage = True
        return isPickerStage
            
    async def execute(self, _times, _threadId):
        self._threadId = _threadId    
        jar = aiohttp.CookieJar(unsafe=True)                  
        async with aiohttp.ClientSession(cookie_jar = jar) as session:
            async with session.get(self.url_initStat, params=self.querystring_initStat, headers=self.headers_initStat, verify_ssl=False) as response:
                resp = await response.text()
                self.processResponse_initStat(resp)
                #self.session = session
                for play_time in range(1, _times+1):
                    _payload1 = self.payload_play.replace("{tid}", self.tid)
                    
                    if self._isPickerStage():
                        if self._getPickerStrategy() == "random":
                            _maxRandom   = int(self._getPickerMaxRandom())
                            _i_maxRandom = randint(0, _maxRandom)
                            self._payload2 = _payload1.replace("{picker_repl}", self.picker_play[ self.nextStage ][ _i_maxRandom ])
                            self._picker   = self.picker_play[ self.nextStage ][ _i_maxRandom ]
                            #print(self._serverId + "|" + self._threadId + "|" + self._taskId + "|" + str(self.play_idx_play) + "|" + self.nextStage + " -> " + self._picker)                             
                        else:
                            self._payload2 = _payload1.replace("{picker_repl}", self.picker_play[ self.nextStage ][ self.stage_idx_play ])
                            self._picker   = self.picker_play[ self.nextStage ][ self.stage_idx_play ]
                            #print(self._serverId + "|" + self._threadId + "|" + self._taskId + "|" + str(self.play_idx_play) + "|" + self.nextStage + " -> " + self._picker)                            
                         
                        self.stage_idx_play += 1                       
                    else:
                        self._payload2 = _payload1.replace("{picker_repl}", "")
                        #self.stage_idx_play = 0
                    
                    async with session.post(self.url_play, params=self.querystring_play, headers=self.headers_play, data=self._payload2, verify_ssl=False) as response:
                        resp = await response.text()
                        self.processResponse_play(resp)
                        self.play_idx_play += 1
                        
                        if not self._isPickerStage_curr():
                            self.stage_idx_play = 0
                        #else:
                        #    self.stage_idx_play = 0                        
                        
                        if play_time % 1000 == 0:
                            print("thread: {0}, task {1}, time {2}".format(self._threadId, self._taskId, play_time))                                
    
    def processResponse_initStat(self, response):
        self.node = etree.fromstring(response)
        _tids = self.node.xpath("//TransactionId/text()")
        if _tids is None or len(_tids) == 0:
            raise Exception(response[0:100])
        else:
            self.tid = _tids[0]
            self.nextStage = self.node.xpath("//NextStage/text()")[0]
            self.currStage = self.node.xpath("//Stage/text()")[0]
            
            #_fileName = "d:\\WSRY_histo_t\\{}#{:09d}#initStat.xml".format(self._taskId, self.play_idx_play)
            _fileName = "{}#{:09d}#initStat.xml".format(self._taskId, self.play_idx_play)
            XMLFileParserInc(response, _fileName, SingleThreadTask.filter_inc, False, True)        
        #print(self._serverId + "|" + self._threadId + "|" + self._taskId  + " -> " + self.tid)

    def processResponse_play(self, response):        
        self.node = etree.fromstring(response)        
        try:
            _tids = self.node.xpath("//OutcomeDetail/TransactionId/text()")
            if _tids is None or len(_tids) == 0:
                raise Exception(response[0:100])
            else:
                self.tid = _tids[0]
                self.nextStage = self.node.xpath("//NextStage/text()")[0]
                self.currStage = self.node.xpath("//Stage/text()")[0]
                #_fileName = "d:\\WSRY_histo_t\\{}#{:09d}.xml".format(self._taskId, self.play_idx_play)
                _fileName = "{}#{:09d}.xml".format(self._taskId, self.play_idx_play) 
                #_fileName = "d:\\WSRY_histo\\"+ self._taskId + "#" +self.tid+".xml"
                XMLFileParserInc(response, _fileName, SingleThreadTask.filter_inc, False, True)
                
        except Exception as e:
            print(self._serverId + "|" + self._threadId + "|" + self._taskId + " -> " + response[0:200])
            print(self._serverId + "|" + self._threadId + "|" + self._taskId + " -> " + self.url_play)
            print(self.querystring_play)
            print(self._payload2)
            print(self.headers_play)
            raise e
        else:
            pass    
            #print(self.tid)  

#     def processResponse_play_1(self, response):               
#         try:
#             idx1 = response.find("<TransactionId>")
#             idx2 = response.find("</TransactionId>")
#             self.tid = response[idx1+15 : idx2]
#         except Exception as e:
#             raise e
#         else:
#             pass    
#             #print(self.tid)

def createSingleThreadTask(server, _initStat_querystring, _initStat_headers, _play_querystring, _play_payload, _play_payload_pickers, _play_headers, _play_id):
    _singleThreadTasks = []    
    for index in range(0, int(server['tasksPerThread'])):
        _url_i          = server['initStat_url']
        _querystring_i  = _initStat_querystring[index]
        _headers_i      = _initStat_headers[index]
        
        _url_p          = server['play_url']
        _querystring_p  = _play_querystring[index]
        _payload_p      = _play_payload[index]
        _picker_p       = _play_payload_pickers[index]
        _header_p       = _play_headers[index] 
        _play_id_task   = _play_id[index]
               
        _task = SingleThreadTask(server['id'], str(index))
        _task.setInitStatParams(_url_i, _querystring_i, _headers_i)
        _task.setPlayParams(_url_p, _querystring_p, _payload_p, _picker_p, _header_p, _play_id_task)        
        _singleThreadTasks.append( _task )
               
    return _singleThreadTasks 

def singleThreadFunc(_singleThreadTasks, _times, _threadId):
    tasks = [ task.execute(_times, _threadId) for task in _singleThreadTasks ]
    evtloop = asyncio.new_event_loop()
    asyncio.set_event_loop(evtloop)        
    loop = asyncio.get_event_loop()
    loop.run_until_complete( asyncio.wait(tasks) )     


if __name__ == "__main__":
    threads = []
    
    d1 = datetime.datetime.now()
    
    for server_id in range(0, len(distr_histo['servers'])):
        server = distr_histo['servers'][server_id]
        for thread_id in range(0, int(server['thread_num'])):                        
            _initStat_querystring = initStat_querystring[ server['server_ip'] ][thread_id]
            _initStat_headers = initStat_headers[ server['server_ip'] ][thread_id]
            
            _play_querystring = play_querystring[ server['server_ip'] ][thread_id]
            _play_payload = play_load[ server['server_ip'] ][thread_id]
            _play_payload_pickers = play_load_picker[ server['server_ip'] ][thread_id]
            _play_headers = play_headers[ server['server_ip'] ][thread_id]
            _play_id = server['play_id'][thread_id]
            
            tasks = createSingleThreadTask(server, _initStat_querystring, _initStat_headers, _play_querystring, _play_payload, _play_payload_pickers, _play_headers, _play_id)         
            th_id = threading.Thread(target=singleThreadFunc, args=(tasks, int(server['spinsPerTask']), str(thread_id)))
            threads.append(th_id)
            th_id.start()
    
    for th_id in threads:
        th_id.join()    
#    threads.clear()

    d2 = datetime.datetime.now()       
    print( "play time:" + str( (d2-d1).seconds ) )   