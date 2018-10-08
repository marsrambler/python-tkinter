'''
@author: Yiz56865
'''
from com.config.config_global import global_conf

from lxml import etree
from xml.dom import minidom

class XMLFileParser:
    def __init__(self, XMLContent, XMLFileName):
        self._fileName = XMLFileName
        self._node = etree.fromstring(XMLContent)        
        self._cont = etree.tostring(self._node, pretty_print=True)
                    
        self._fmtc = minidom.parseString(self._cont).toprettyxml(indent="  ")
        with open(global_conf.storage+"\\tmp_response.txt", 'w') as doc:
            doc.write(self._fmtc)
         
        newdoc = open(self._fileName, 'w');
        with open(global_conf.storage+"\\tmp_response.txt", 'r') as doc:
            for line in doc.readlines():
                newline = line.strip();
                if len(newline) == 0:
                    pass;
                else:
                    newdoc.write(line)        
            
    def getText(self, xpath):
        for quote in self._node.xpath(xpath+"/text()"):
            return quote;
    
    def getAttr(self, xpath):
        for quote in self._node.xpath(xpath):
            return quote;
                

class XMLFileFilter:
    def __init__(self, origFileName, destFileName, filter):
        _rootTree = etree.parse(origFileName)
        _rootElement = _rootTree.getroot()
        for flt in filter:
            if flt.startswith("#"):
                continue
            bads = _rootElement.xpath(flt)
            for bd in bads:
                bd.getparent().remove(bd)
                
        _cont = etree.tostring(_rootElement, pretty_print=True)
        _fmtc = minidom.parseString(_cont).toprettyxml(indent="  ")
        
        with open(global_conf.storage+"\\tmp_response.txt", 'w') as doc:
            doc.write(_fmtc)

        newdoc = open(destFileName, 'w');
        with open(global_conf.storage+"\\tmp_response.txt", 'r') as doc:
            for line in doc.readlines():
                newline = line.strip();
                if len(newline) == 0:
                    pass;
                else:
                    newdoc.write(line)  
                    
class XMLFileFilterInc:
    def __init__(self, origFileName, destFileName, filter):
        _rootTree = etree.parse(origFileName)
        _rootElement = _rootTree.getroot()
        _reserve = []
        for flt in filter:
            if flt.startswith("#"):
                continue
            goods = _rootElement.xpath(flt)
            for gd in goods:
                _reserve.append(gd)
        
        _children = _rootElement.getchildren()
        for chd in _children:
            if chd in _reserve:
                pass
            else:
                _rootElement.remove(chd) 
                
        _cont = etree.tostring(_rootElement, pretty_print=True)
        _fmtc = minidom.parseString(_cont).toprettyxml(indent="  ")
        
        with open(global_conf.storage+"\\tmp_response.txt", 'w') as doc:
            doc.write(_fmtc)

        newdoc = open(destFileName, 'w');
        with open(global_conf.storage+"\\tmp_response.txt", 'r') as doc:
            for line in doc.readlines():
                newline = line.strip();
                if len(newline) == 0:
                    pass;
                else:
                    newdoc.write(line)

class XMLFileParserInc:
    
    import redis
    redis_conn = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    def __init__(self, XMLContent, XMLFileName, filter, persistDisk=False, persistRedis=False):
        self._fileName = XMLFileName
        self._node = etree.fromstring(XMLContent)        
        
        _reserve = []
        for flt in filter:
            if flt.startswith("#"):
                continue
            goods = self._node.xpath(flt)
            for gd in goods:
                _reserve.append(gd)
        
        _children = self._node.getchildren()
        for chd in _children:
            if chd in _reserve:
                pass
            else:
                self._node.remove(chd)
                                
        self._cont = etree.tostring(self._node, pretty_print=True)
        
        if persistDisk:                    
            self._fmtc = minidom.parseString(self._cont).toprettyxml(indent="  ")
            with open(self._fileName, 'w') as doc:
                doc.write(self._fmtc)
        if persistRedis:
            XMLFileParserInc.redis_conn.set(XMLFileName, self._cont) 
                    
if __name__ == "__main__":
    #inc = XMLFileFilterInc("C:\\rgs_ddi_workFlow\\origStore\\play_A74M@-15362024764861.xml", "d:\\dest.xml", ["//OutcomeDetail", "//AwardCapOutcome"])
    #print(inc)
    #_cont = "<a> <b> </b> <c>_cont </c></a>"
    #XMLFileParserInc(_cont, "c:\\own_file.txt", ["//c",])
    import redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.set('name', 'junxi')
    
    
    
                        