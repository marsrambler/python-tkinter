'''
Created on Jul 31, 2018

@author: yiz
'''

import os
from lxml import etree
from xml.dom import minidom
from com.config.config_global import global_conf
from com.config.config import gem_configs
import glob
from subprocess import Popen, PIPE
from shutil import copyfile
import threading
import datetime

def _transForceHtml_thread(payt, forceHtml, newf):
    dom  = etree.parse(payt)
    xslt = etree.parse(forceHtml)
    tran = etree.XSLT(xslt)
    newdom = tran(dom)
    cont = etree.tostring(newdom, method="html", pretty_print=True)
#    fmct = minidom.parseString(cont).toprettyxml(indent="  ", newl="")
    with open(newf, 'w') as doc:
        doc.write(cont.decode("utf-8"))
#        doc.write(fmct)    

def _transForceHtml():
    htmls = []
    threadIds = []
    paytables, forceHtml, forceXml, paytrans, r5, r6, r7, r8, r9 = _getPaytableFiles()
    for payt in paytables:        
        idx = payt.rfind("\\")
        f = payt[idx+1:]
        idx = f.rfind("-")
        f1 = f[0:idx]
        newf = gem_configs.origStore + "\\..\\" + f1 + "-Force.html"            
        htmls.append(newf)
        th = threading.Thread(target=_transForceHtml_thread, args=(payt, forceHtml, newf))
        th.start()
        threadIds.append(th)
    return htmls, threadIds 

def _transForceXml_thread(payt, forceXml, newf):
    dom  = etree.parse(payt)
    xslt = etree.parse(forceXml)
    tran = etree.XSLT(xslt)
    newdom = tran(dom)
    cont = etree.tostring(newdom, pretty_print=True)
    fmct = minidom.parseString(cont).toprettyxml(indent="  ", newl="")
    with open(newf, 'w') as doc:
        doc.write(fmct)        
        
def _transForceXml():
    xmls = []
    threadIds = []
    paytables, forceHtml, forceXml, paytrans, r5, r6, r7, r8, r9 = _getPaytableFiles()
    for payt in paytables:
        idx = payt.rfind("\\")
        f = payt[idx+1:]
        idx = f.rfind("-")
        f1 = f[0:idx]
        newf = gem_configs.origStore + "\\..\\" + f1 + "-Force.xml"            
        xmls.append(newf)
        th = threading.Thread(target=_transForceXml_thread, args=(payt, forceXml, newf))     
        th.start()
        threadIds.append(th)
    return xmls, threadIds

def _transPaytables_thread(payt, paytrans, newf):
    dom  = etree.parse(payt)
    xslt = etree.parse(paytrans)
    tran = etree.XSLT(xslt)
    newdom = tran(dom)
    cont = etree.tostring(newdom, pretty_print=True)
    fmct = minidom.parseString(cont).toprettyxml(indent="  ", newl="")
    with open(newf, 'w') as doc:
        doc.write(fmct)        
        
def _transPaytables():
    helpers = []
    threadIds = []
    paytables, forceHtml, forceXml, paytrans, r5, r6, r7, r8, r9 = _getPaytableFiles()
    for payt in paytables:        
        idx = payt.rfind("\\")
        f = payt[idx+1:]
        idx = f.rfind("-")
        f1 = f[0:idx]
        newf = gem_configs.origStore + "\\..\\" + f1 + "-PaytableHelp.xml"     
        helpers.append(newf)
        th = threading.Thread(target=_transPaytables_thread, args=(payt, paytrans, newf))
        th.start()
        threadIds.append(th)
    return helpers, threadIds    

def _getPaytableFiles():
    files = os.listdir(global_conf.paytable_dir)
    paytables = []
    forceHtml = None
    forceXml = None
    paytableTrans = None
    inits = []
    ghsts = []
    filter = None
    mapping = None
    stage = None
    for file in files:
        if not os.path.isfile(global_conf.paytable_dir + "\\" + file): 
            pass;
        elif file.find("-Paytable.xml") != -1:
            paytables.append(global_conf.paytable_dir + "\\" + file)
        elif file.find("-ForceHtml.xsl") != -1:
            forceHtml = global_conf.paytable_dir + "\\" + file
        elif file.find("-ForceXml.xsl") != -1:
            forceXml = global_conf.paytable_dir + "\\" + file
        elif file.find("-Paytable.xsl") != -1:
            paytableTrans = global_conf.paytable_dir + "\\" + file
        elif file.find("-Init.xml") != -1:
            inits.append(global_conf.paytable_dir + "\\" + file)
        elif file.find("-Ghst") != -1:
            ghsts.append(global_conf.paytable_dir + "\\" + file)
        elif file.find("-Filter.xml") != -1:
            filter = global_conf.paytable_dir + "\\" + file
        elif file.find("-Mapping.xml") != -1:
            mapping = global_conf.paytable_dir + "\\" + file
        elif file.find("-Stage.xml") != -1:
            stage = global_conf.paytable_dir + "\\" + file
    return paytables, forceHtml, forceXml, paytableTrans, inits, ghsts, filter, mapping, stage

def _signPaytables_thread(sign_cmd):
    for line in os.popen(sign_cmd):
        print(line)        

def _signPaytables():    
    sign_tool = os.path.dirname(__file__) + "\\devSigner.jar"    
    signeds = []
    threadIds = []
    paytables, forceHtml, forceXml, paytrans, r5, r6, r7, r8, r9 = _getPaytableFiles()    
    for payt in paytables:        
        idx = payt.rfind("\\")
        f = payt[idx+1:]
        idx = f.rfind("-")
        f1 = f[0:idx]
        newf = gem_configs.origStore + "\\..\\" + f1 + "-Paytable.xml"
        sign_cmd = "java -jar {0} {1} {2}".format(sign_tool, payt, newf)
        signeds.append(newf)     
        th = threading.Thread(target=_signPaytables_thread, args=(sign_cmd, ))
        th.start()
        threadIds.append(th)
    return signeds, threadIds      

def _copyInits():
    copieds = []
    r1, r2, r3, r4, inits, r6, r7, r8, r9 = _getPaytableFiles()
    for init in inits:
        idx = init.rfind("\\")
        f = init[idx+1:]
        newf = gem_configs.origStore + "\\..\\" + f
        copyfile(init, newf)
        copieds.append(newf)     
    
    return copieds, None            

def _copyGhsts():
    copieds = []
    r1, r2, r3, r4, r5, ghsts, r7, r8, r9 = _getPaytableFiles()
    for ghst in ghsts:
        idx = ghst.rfind("\\")
        f = ghst[idx+1:]
        newf = gem_configs.origStore + "\\..\\" + f
        copyfile(ghst, newf)
        copieds.append(newf)     
    
    return copieds, None    

def _copyFilter():
    r1, r2, r3, r4, r5, r6, filter, r8, r9 = _getPaytableFiles()
    idx = filter.rfind("\\")
    f = filter[idx+1:]
    newf = gem_configs.origStore + "\\..\\" + f
    copyfile(filter, newf)
    return newf, None

def _signMapping_thread(sign_cmd):
    for line in os.popen(sign_cmd):
        print(line)
        
def _signMapping():    
    sign_tool = os.path.dirname(__file__) + "\\devSigner.jar"    
    r1, r2, r3, r4, r5, r6, r7, mapping, r9 = _getPaytableFiles()    
    
    threadIds = []   
    idx = mapping.rfind("\\")
    f = mapping[idx+1:]
    newf = gem_configs.origStore + "\\..\\" + f
    sign_cmd = "java -jar {0} {1} {2}".format(sign_tool, mapping, newf)
    th = threading.Thread(target=_signMapping_thread, args=(sign_cmd, ))
    th.start()
    threadIds.append(th)        
    return newf, threadIds

def _signStage_thread(sign_cmd):
    for line in os.popen(sign_cmd):
        print(line)
        
def _signStage():    
    sign_tool = os.path.dirname(__file__) + "\\devSigner.jar"    
    r1, r2, r3, r4, r5, r6, r7, r8, stage = _getPaytableFiles()    
    
    threadIds = []    
    idx = stage.rfind("\\")
    f = stage[idx+1:]
    newf = gem_configs.origStore + "\\..\\" + f
    sign_cmd = "java -jar {0} {1} {2}".format(sign_tool, stage, newf)
    th = threading.Thread(target=_signStage_thread, args=(sign_cmd, ))
    th.start()
    threadIds.append(th)     
            
    return newf, threadIds    

def _getGameFileFromTomcat():
    idx = global_conf.softwareId.rfind("-")
    name = global_conf.softwareId[0 : idx]
    files = glob.glob(global_conf.tomcat+"\\webapps\\rgslite\\**\\" + name + "*", recursive=True)
    
    rem_files = {}
    for file in files:
        idx = file.rfind("\\")
        rem_files[file[ idx+1 : ]] = file
        
    return rem_files
    
Func_array = [_transForceHtml, _transForceXml, _transPaytables, _signPaytables, _copyInits, _copyGhsts, _copyFilter, _signMapping, _signStage]

def _build_all_paytables():    
    genfiles = []
    threads  = []
    for func in Func_array:
        res, ths = func()
        if isinstance(res, list):
            genfiles += res
        else:
            genfiles += [res, ]
        
        if ths is not None:
            threads += ths
                    
    return genfiles, threads
    
def _updateConfig_thread():    
    dstf = global_conf.tomcat + "\\webapps\\rgslite\\WEB-INF\\classes\\additionalConfiguration.xml"    
    addiCfg = etree.parse(dstf)
    
    gleCfg = etree.parse(global_conf.paytable_dir + "\\GLEConfig.xml")
    gameId = gleCfg.xpath('//family/@code')[0] + '0'
    
    ELM = addiCfg.xpath('//game[@id='+gameId+']')
    if len(ELM) > 0:
        pass;
    else:
        cont = '''
            <game id="{0}">
                <languageCodes/>
            </game>
        '''.format(gameId)
        
        node = etree.fromstring(cont)
        
        ELM_p = addiCfg.xpath('//language')
        idx = len(ELM_p[0].getchildren())
        ELM_p[0].insert(idx, node)
        
        cont = etree.tostring(addiCfg, pretty_print=True)
        fmct = minidom.parseString(cont).toprettyxml(indent="", newl="")
        
        newf = gem_configs.origStore + "\\..\\" + "additionalConfiguration.xml"
        
        with open(newf, "w") as doc:
            doc.write(fmct)
        
        copyfile(newf, dstf)    

def _updateConfig():
    threads = []
    th = threading.Thread(target=_updateConfig_thread)
    th.start()
    threads.append(th)
    return None, threads

def _updateGameData_tread():
    dstf = global_conf.tomcat + "\\webapps\\rgslite\\WEB-INF\\classes\\localgamedata.xml"
        
    gleCfg = etree.parse(global_conf.paytable_dir + "\\GLEConfig.xml")
    code = gleCfg.xpath('//family/@code')[0]
    gameId = code + '0'    
    gameName = gleCfg.xpath('//game/@name')[0]
    
    softwareIds = gleCfg.xpath('//paymodel/@modelid')
    paymodelIds = []
    for id in softwareIds:
        paymodelIds.append( id.replace("-", "") )
    paymodelNames = gleCfg.xpath('//paymodel/@name')    
    gameFolder = gleCfg.xpath('//presentation/@gameFolder')[0]    
    
    gmdata = etree.parse(dstf)    
    ELM = gmdata.xpath('//games/game/gameid[contains(text(),' + gameId + ')]')    
    
    if len(ELM) > 0:
        pass;
    else:
        cont = '''
        <game>
            <gameid>{0}</gameid>
            <gamefamily>{1}</gamefamily>
            <gamenumber>0</gamenumber>
            <gamename>{2}</gamename>
            <gamedesc>SlotGame</gamedesc>
            <jackpotid/>
            <jackpotType/>
            <prevstateloadind>Y</prevstateloadind>
            <studio>ddi</studio>
            <gameType>S</gameType>
            <gameOptions/>
            <enableFreeSpin/>
            <gamelogicversion>1.0</gamelogicversion>
            <betMultipliers>1,4,20,100</betMultipliers>
        </game>        
        '''.format(gameId, code, gameName)        
        
        node = etree.fromstring(cont)
        
        ELM_p = gmdata.xpath('//games')[0]
        idx = len(ELM_p.getchildren())
        ELM_p.insert(idx, node)
        
        for index in range(len(softwareIds)):
            cont = '''
            <paymodel>
                <paymodelid>{0}</paymodelid>
                <softwareid>{1}</softwareid>
                <paymodelname>{2}</paymodelname>
                <gameid>{3}</gameid>
                <hibethold>4.94</hibethold>
                <lobethold>4.94</lobethold>
                <hisidbet>4.94</hisidbet>
                <losidbet>4.94</losidbet>
                <threshcoinsnbr>1</threshcoinsnbr>
                <conflevel>91.97</conflevel>
                <fixedminmax>Y</fixedminmax>
                <mincoin>1</mincoin>
                <maxcoin>40</maxcoin>
                <maxmainbetwin>2500</maxmainbetwin>
                <maxsidebetwin>1000</maxsidebetwin>
            </paymodel>        
            '''.format(paymodelIds[index], softwareIds[index], paymodelNames[index], gameId)
        
            node = etree.fromstring(cont)
            
            ELM_p = gmdata.xpath('//gamedata/paymodels')[0]
            idx = len(ELM_p.getchildren())
            ELM_p.insert(idx, node)
        
        for index in range(len(softwareIds)):
            cont = '''
                <selection>
                    <selectionid>{0}</selectionid>
                    <skincode>DDI-SKIN1</skincode>
                    <enabled>Y</enabled>
                    <gameid>{1}</gameid>
                    <softwareid>{2}</softwareid>
                    <maxbetamt>40</maxbetamt>
                    <minbetamt>1</minbetamt>
                    <maxsidebetamt>333</maxsidebetamt>
                    <minsidebetamt>1</minsidebetamt>
                    <defaultminbet>0.5</defaultminbet>
                    <denoms>
                        <denom>
                            <denomid>3342</denomid>
                            <betMultipliers>1,4,20,100</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                    </denoms>
                    <types>
                        <type>
                            <presentation>FLSH</presentation>
                            <channel>INT</channel>
                            <height>768</height>
                            <width>1024</width>
                            <meterheight>0</meterheight>
                            <meterwidth>0</meterwidth>
                            <gameFolder>{3}</gameFolder>
                        </type>
                        <type>
                            <presentation>HTML</presentation>
                            <channel>MOB</channel>
                            <height>768</height>
                            <width>1024</width>
                            <meterheight>0</meterheight>
                            <meterwidth>0</meterwidth>
                            <gameFolder>{4}</gameFolder>
                        </type>
                    </types>
                </selection>            
            '''.format(paymodelIds[index], gameId, softwareIds[index], gameFolder, gameFolder)
            
            node = etree.fromstring(cont)
            
            ELM_p = gmdata.xpath('//selections')[0]
            idx = len(ELM_p.getchildren())
            ELM_p.insert(idx, node)            
            
            cont = '''
                <selection>
                    <selectionid>{0}</selectionid>
                    <skincode>DDIT</skincode>
                    <enabled>Y</enabled>
                    <gameid>{1}</gameid>
                    <softwareid>{2}</softwareid>
                    <maxbetamt>40</maxbetamt>
                    <minbetamt>1</minbetamt>
                    <maxsidebetamt>333</maxsidebetamt>
                    <minsidebetamt>1</minsidebetamt>
                    <defaultminbet>0.5</defaultminbet>
                    <denoms>
                        <denom>
                            <denomid>3315</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                        <denom>
                            <denomid>3316</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                        <denom>
                            <denomid>3317</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                        <denom>
                            <denomid>3318</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                        <denom>
                            <denomid>3319</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                        <denom>
                            <denomid>3320</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                        <denom>
                            <denomid>3321</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                        <denom>
                            <denomid>3322</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                        <denom>
                            <denomid>3323</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                        <denom>
                            <denomid>3324</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                        <denom>
                            <denomid>3325</denomid>
                            <betMultipliers>1</betMultipliers>
                            <enabled>Y</enabled>
                        </denom>
                    </denoms>
                    <types>
                        <type>
                            <presentation>FLSH</presentation>
                            <channel>INT</channel>
                            <height>768</height>
                            <width>1024</width>
                            <meterheight>0</meterheight>
                            <meterwidth>0</meterwidth>
                            <gameFolder>{3}</gameFolder>
                        </type>
                        <type>
                            <presentation>HTML</presentation>
                            <channel>MOB</channel>
                            <height>768</height>
                            <width>1024</width>
                            <meterheight>0</meterheight>
                            <meterwidth>0</meterwidth>
                            <gameFolder>{4}</gameFolder>
                        </type>
                    </types>
                </selection>            
            '''.format(paymodelIds[index], gameId, softwareIds[index], gameFolder, gameFolder)
            
            node = etree.fromstring(cont)
            
            ELM_p = gmdata.xpath('//selections')[0]
            idx = len(ELM_p.getchildren())
            ELM_p.insert(idx, node)
                           
        cont = etree.tostring(gmdata, pretty_print=True)
        fmct = minidom.parseString(cont).toprettyxml(indent="", newl="")
        
        newf = gem_configs.origStore + "\\..\\" + "localgamedata.xml"        
        
        with open(newf, "w") as doc:
            doc.write(fmct)
        
        copyfile(newf, dstf)

def _updateGameData():
    threads = []
    th = threading.Thread(target=_updateGameData_tread)
    th.start()
    threads.append(th)
    return None, threads


Func_array_wrapper = [_updateGameData, _updateConfig, _build_all_paytables]

def _build_paytables_wrapper_func():
    files   = []
    threads = []
    for func in Func_array_wrapper:
        f, t = func()
        if f is not None:
            files += f
        if t is not None:
            threads += t
    
    for th in threads:
        th.join()
        
    gened = {}
    for file in files:
        idx = file.rfind("\\")
        gened[file[ idx+1 : ]] = file
    
    copied = []
    
    for fname in gened.keys():
        if fname.find("-Filter.xml") != -1 or fname.find("-Mapping.xml") != -1 or fname.find("-Stage.xml") != -1:
            file_dst = global_conf.tomcat + "\\webapps\\rgslite\\WEB-INF\\classes\\game\\configs\\" + fname
        elif fname.find("-Init.xml") != -1 or fname.find("-Paytable.xml") != -1 or fname.find("-PaytableHelp.xml") != -1:
            file_dst = global_conf.tomcat + "\\webapps\\rgslite\\WEB-INF\\classes\\game\\paymodels\\" + fname
        elif fname.find("-Ghst") != -1:
            file_dst = global_conf.tomcat + "\\webapps\\rgslite\\WEB-INF\\classes\\game\\transforms\\" + fname
        elif fname.find("-Force.html") != -1 or fname.find("-Force.xml") != -1:
            file_dst = global_conf.tomcat + "\\webapps\\rgslite\\WEB-INF\\classes\\gleForce\\" + fname
                                        
        file_src = gened[fname]
        copyfile(file_src, file_dst)    
        copied.append(fname)
    
    key1 = gened.keys()
    key2 = set(copied)
    diff = list(key1 - key2)
    
    if len(diff) > 0:
        print("Error, below file not copied to tomcat: \n" + diff)    

def _build_paytables_func(progBar, root):
    try:
        tr = threading.Thread(target=_build_paytables_wrapper_func)
        tr.start()
        while True:
            tr.join(0.2)
            progBar.step(20)
            progBar.update_idletasks()
            root.update_idletasks()
            if not tr.isAlive():
                break;
        
    except:
        print("Error in _build_paytables_func")
    
    progBar["value"]=100
    progBar.update_idletasks()      
        
def build_paytables_func(progBar, root):
    try:
        t = threading.Thread(target=_build_paytables_func, args=(progBar, root))
        t.start()
    except:
        print("Error in start build pay table")
    
if __name__ == "__main__":
    d1 = datetime.datetime.now()
    _build_paytables_wrapper_func()
    d2 = datetime.datetime.now()
    print( (d2-d1).seconds )
    
    