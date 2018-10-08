'''
Created on Jul 23, 2018

@author: yiz
'''

from com.config.config_global import global_conf

gem_configs = {
             'title': 'own game',
             'width': '1024',
             'height': '768',
             'geometry': '1024x768',
             'origStore': global_conf.storage + '\\origStore\\',
             'workStore': global_conf.storage + '\\workStore\\',
             'workStore_inc': global_conf.storage + '\\workStore_inc\\',
             'workRecord': global_conf.storage + '\\work_recored.log',
             'filterFile': global_conf.storage + '\\filter.cfg',
             'filterFile_inc': global_conf.storage + '\\filter_inc.cfg'             
             }

xml_disp_configs = {
            'name': 'red',
            'stripIndex': 'red',
            'stage': 'red',
            'key': 'red',
            'value': 'red',
            'stageConnector': 'red'
          }

initStat_url = {
            'url' : global_conf.prot + "://" + global_conf.ip + ":" + global_conf.port + global_conf.webapp + "/tc/initstate"
          }

initStat_querystring = {"":"",
 }
initStat_headers = {
                        'cache-control': "no-cache",
                        'postman-token': "fe8f40d3-0e7c-71b0-d992-340eec97c89d"
                    }

paytable_url = {
              'url': global_conf.prot + "://" + global_conf.ip + ":" + global_conf.port + global_conf.webapp + "/tc/paytable"
            }

paytable_querystring = {"":"","showInitialCashier":"false","parametersFromConfigCall":"true","nscashout":"","defaultbuyinamount":"1000.0",
                        "softwareid":global_conf.softwareId,"language":"en","countrycode":"US","istournament":"false","nscode":"DDI","denomid":"3342",
                        "audio":"on","skincode":"DDI-SKIN1","minbet":"333","ipaddress":global_conf.ip,"moduleAssetPath":"/gpe","affiliate":"",
                        "uniqueid":global_conf.uniqueid,"time":"1499076423169"                        
                }

paytable_headers = {
        'cache-control': "no-cache",
        'postman-token': "07dc8c5d-8af0-0066-b8b0-148f05429cbb"                    
                }

play_url = {
            'url': global_conf.prot + "://" + global_conf.ip + ":" + global_conf.port + global_conf.webapp + "/tc/play"
        }

play_querystring = {
                    "":"","showInitialCashier":"false","parametersFromConfigCall":"true","nscashout":"","defaultbuyinamount":"1000.0",
                    "softwareid":global_conf.softwareId,"language":"en","countrycode":"US","istournament":"false","nscode":"DDI","denomid":"3342",
                    "skincode":"DDI-SKIN1","minbet":"333","ipaddress":global_conf.ip,"moduleAssetPath":"/gpe","affiliate":"","uniqueid":global_conf.uniqueid,
                    "time":"1499076461333"
                }

play_payload = {
                'payload' : 
                
                '<GameLogicRequest>\n  \
                    <TransactionId>{tid}</TransactionId>\n  \
                    <PatternSliderInput>\n    \
                        <BetPerPattern>' + global_conf.BetPerPattern + '</BetPerPattern>\n    \
                        <PatternsBet>' + global_conf.PatternsBet + '</PatternsBet>\n  \
                    </PatternSliderInput>\n  \
                    {picker_repl}\n \
                </GameLogicRequest>'
                }

play_payload_picker = {
                    'payload':
                    
                    '<PickerInput>\n    \
                        <Pick name=\"{picker_name}\"/>\n  \
                    </PickerInput>'
                }

play_headers = {
                'cache-control': "no-cache",
                'postman-token': "b90a76d7-bf05-4dcf-3388-6700aed7e1c1" 
            }

force_path = {
              'url': global_conf.prot + "://" + global_conf.ip + ":" + global_conf.port + global_conf.webapp + "/tc/ForceServlet/INT_FLSH_" + global_conf.softwareId + "/" + global_conf.uniqueid
            }    