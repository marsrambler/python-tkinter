'''
Created on Aug 3, 2018

@author: yiz
'''

import os
from lxml import etree

path = "D:\\rgs_ddi_workspace\\repo_gle_core\\paytable\\TripleHotIce\\histo_result\\"

if __name__ == "__main__":
    files = os.listdir(path)
    idx = 0
    for file in files:
        if os.path.isfile(path + file) and file.find(".xml") != -1:
            idx += 1000000
            dom = etree.parse(path + file)
            
            wager = float(dom.xpath("//Wager/text()")[0])
            base  = float(dom.xpath("//Pay_Lines/text()")[0])
            
            free0 = dom.xpath("//FS_Line_pay_F/text()")[0]
            free1 = dom.xpath("//FS_Line_pay_F/text()")[1]
            
            free = float(free0) + float(free1)            
            
            wheel0 = dom.xpath("//Wheel_Slice_pay_W/text()")[0]
            wheel1 = dom.xpath("//Wheel_Slice_pay_W/text()")[1]
            
            credit = float(dom.xpath("//Credits_pay_P/text()")[0])
            boost  = float(dom.xpath("//Boost_pay_P/text()")[0])
            base_p = float(dom.xpath("//Base_pay_P/text()")[0])
            contr1 = float(dom.xpath("//Contribution_pay_P/text()")[0])
            
            f0 = float(wheel0)
            f1 = float(wheel1)
            if f0 > f1:
                contr0 = f1
                wheel = f0
            else:
                contr0 = f0
                wheel = f1                        
            
            contr = contr0 + contr1
            pick = credit + boost + base_p
            
            total = base + free + wheel + pick + contr
            
            out = '''{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13}\n'''.format(idx, wager, base, free, wheel, pick, contr, total, base/wager, free/wager, wheel/wager, pick/wager, contr/wager, total/wager)
            #with open("c:\\001.csv", "w") as file:            
            #print(idx+","+wager+","+base+","+free+","+wheel+","+pick+","+contr+","+total+","+base/wager+","+free/wager+","+wheel/wager+","+pick/wager+","+contr/wager+","+total/wager)
            with open("c:\\TripleHotIce-001.csv", "a") as file:
                file.write(out)
            
            
        else:
            pass;