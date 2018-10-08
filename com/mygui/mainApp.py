'''
Created on Jul 23, 2018

@author: yiz
'''

#
# Laying out a tkinter grid
#
# Please also find two images:
#    GridLayout.png and screenshot.png
# Credit: Modified by Larz60+ From the original:
#    'http://www.tkdocs.com/tutorial/grid.html'
#
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from com.config.config import gem_configs
from com.config.config_global import global_conf
from com.mygui.initStat_func import initStat_func
from com.mygui.getPayTable_func import getPayTable_func
from com.mygui.play_func import play_func
from com.config.config import xml_disp_configs
from com.config.config import force_configs
from com.mygui.LXmlParser import XMLFileFilter, XMLFileFilterInc
from com.mygui.tomcat_manage import tomcat_start, tomcat_stop, tomcat_running, tomcat_deploy
from com.mygui.ant_build import ant_build_social
from com.mygui.ant_histo import ant_run_histo
import difflib
import webbrowser
import tkinter
from tkinter.ttk import Progressbar
from com.mygui.build_paytable import build_paytables_func
from com.mygui.ant_build import ant_build_glecomponent
from com.utils.proxy_util import disable_proxy_in_env_var, disable_ie_proxy, enable_ie_proxy


class Text2(Frame):
    def __init__(self, master, width=0, height=0, **kwargs):
        self.width = width
        self.height = height

        Frame.__init__(self, master, width=self.width, height=self.height)
        self.text_widget = Text(self, **kwargs)
        self.text_widget.pack(expand=YES, fill=BOTH)

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

    def grid(self, *args, **kwargs):
        Frame.grid(self, *args, **kwargs)
        self.grid_propagate(False)

class TextWithMenu(Text):
    def __init__(self, master=None, cnf={}, **kw):
        Text.__init__(self, master, cnf, **kw)
        self.popup_menu = tkinter.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Fitler out", command=self.filter_out)
        self.popup_menu.add_command(label="Filter in", command=self.filter_in)
        self.bind("<Button-3>", self.popup) # Button-2 on Aqua
        
    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def filter_out(self):
        content = self.selection_get().lstrip().rstrip()
        _elements = content.split(" ")
        _xpath = "//{}".format(_elements[0].replace("<", ""))
        _params = _elements[1:]
        for _pam in _params:
            if _pam.find("name") == -1:
                pass
            else:
                _xpath = "{0}[@{1}]".format(_xpath, _pam)

        with open(gem_configs.filterFile, 'a') as doc:
            doc.write(_xpath + "\n")
                                        
        print('"{}" add into filter out list'.format(_xpath))

    def filter_in(self):
        content = self.selection_get().lstrip().rstrip()
        _elements = content.split(" ")
        _xpath = "//{}".format(_elements[0].replace("<", ""))
        _params = _elements[1:]
        for _pam in _params:
            if _pam.find("name") == -1:
                pass
            else:
                _xpath = "{0}[@{1}]".format(_xpath, _pam)

        with open(gem_configs.filterFile_inc, 'a') as doc:
            doc.write(_xpath + "\n")
                                        
        print('"{}" add into filter in list'.format(_xpath))                
        
        
class MyDialog_V2(Toplevel):
    def __init__(self, parent, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
        self.initial_focus.focus_set()
        self.wait_window(self)
    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        self.lab0 = Label(master, text="Below item will Not be displayed:")
        self.lab0.pack(padx=1, pady=1, side=TOP)
        
        # self.textCtrl = Text(master, background="White", borderwidth=2)
        # self.textCtrl.pack(padx=1, pady=1, side=TOP)
        
        self._textCtrl = Text2(master, width=600, height=300)
        self._textCtrl.pack()
        self.textCtrl = self._textCtrl.text_widget        
        
        self.lab1 = Label(master, text="Below item will be displayed:")
        self.lab1.pack(padx=1, pady=1, side=TOP)
        
        self._textCtrl_inc = Text2(master, width=600, height=300)
        self._textCtrl_inc.pack()
        self.textCtrl_inc = self._textCtrl_inc.text_widget
        
        # self.textCtrl_inc = Text2(master, background="White", borderwidth=2)
        # self.textCtrl_inc.pack(padx=1, pady=5, side=RIGHT)
        
        with open(gem_configs.filterFile, 'r') as doc:
            for line in doc.readlines():
                newline = line.strip()
                self.textCtrl.insert(END, newline + "\n")

        with open(gem_configs.filterFile_inc, 'r') as doc:
            for line in doc.readlines():
                newline = line.strip()
                self.textCtrl_inc.insert(END, newline + "\n")
                        
        return self.textCtrl

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(self)
        
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        # self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    #
    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
    #
    # command hooks
    def validate(self):
        return 1  # override

    def apply(self):
        content = self.textCtrl.get("1.0", END)
        lines = content.split("\n")
        with open(gem_configs.filterFile, 'w') as doc:
            for line in lines:
                newline = line.strip()
                if len(newline) == 0:
                    pass;
                else:
                    doc.write(newline + "\n")

        content = self.textCtrl_inc.get("1.0", END)
        lines = content.split("\n")
        with open(gem_configs.filterFile_inc, 'w') as doc:
            for line in lines:
                newline = line.strip()
                if len(newline) == 0:
                    pass;
                else:
                    doc.write(newline + "\n")

class ResizableWindow:
    
    def __init__(self, parent):
        self.parent = parent
        self.f1_style = ttk.Style()
        self.f1_style.configure('My.TFrame', background='#334353')
        self.f1 = ttk.Frame(self.parent, style='My.TFrame', padding=(3, 3, 3, 3))  # added padding
        self.f1.grid(column=0, row=0, sticky=(N, S, E, W))  # added sticky
        
        # frame produce
        
        self.f_top = ttk.Frame(self.f1, style='My.TFrame', borderwidth=5, relief="sunken")        
        self.f_top.grid(column=0, row=0, columnspan=5, sticky=(N, S, E, W))
                        
        self.f_mid = ttk.Frame(self.f1, borderwidth=5, relief="sunken", width=500, height=800)
        self.f_mid.grid(column=0, row=1, columnspan=3, rowspan=2, sticky=(N, S, E, W))  # added sticky
        
        self.f_rig = ttk.Frame(self.f1, borderwidth=5, relief="sunken", height=800)
        self.f_rig.grid(column=3, row=1, columnspan=2, rowspan=2, sticky=(N, S, E, W))
        
        self.f_bom = ttk.Frame(self.f1, style='My.TFrame', borderwidth=5, relief="sunken")
        self.f_bom.grid(column=0, row=3, columnspan=5, sticky=(N, S, E, W))
        
        # LabFrame 1 in top frame
        self.lab_style = ttk.Style()
        self.lab_style.configure('My.TLabelframe', background='#334353', borderwidth=0)
        self.lab_style.configure('My.TLabelframe.Label', background='#334353', foreground='white', borderwidth=0)
        self.labFrame1 = ttk.Labelframe(self.f_top, style='My.TLabelframe', text="Basic", padding=(2, 2, 2, 2))
        self.labFrame1.grid(column=0, row=0, rowspan=3, columnspan=5, sticky=(N, S, E, W), pady=1, padx=1)

        self.labFrame2 = ttk.Labelframe(self.f_top, style='My.TLabelframe', text="Advance", padding=(2, 2, 2, 2))
        self.labFrame2.grid(column=7, row=0, rowspan=3, columnspan=5, sticky=(N, S, E, W), pady=1, padx=1)

        self.labFrame3 = ttk.Labelframe(self.f_top, style='My.TLabelframe', text="Status", padding=(10, 10, 10, 10))
        self.labFrame3.grid(column=5, row=0, rowspan=3, columnspan=2, sticky=(N, S, E, W), pady=1, padx=10)
                
        # top button
        
        self.btn_initState = ttk.Button(self.labFrame1, text="initState", command=self.initStat_func)
        self.btn_initState.grid(column=0, row=0, sticky=(N, S, E, W), pady=2, padx=2)
        
        self.btn_getPayTable = ttk.Button(self.labFrame1, text="getPayTable", command=self.getPayTable_func)
        self.btn_getPayTable.grid(column=1, row=0, sticky=(N, S, E, W), pady=2, padx=2)
        
        self.btn_play = ttk.Button(self.labFrame1, text="play", command=self.play_func)
        self.btn_play.grid(column=2, row=0, sticky=(N, S, E, W), pady=2, padx=2)
        
        self.btn_force = ttk.Button(self.labFrame1, text="foreTool", command=self.forceTool_func)
        self.btn_force.grid(column=3, row=0, sticky=(N, S, E, W), pady=2, padx=2)
        
        self.btn_build = ttk.Button(self.labFrame1, text="build package-lite", command=self.build_package_lite_func)
        self.btn_build.grid(column=0, row=1, sticky=(N, S, E, W), pady=2, padx=2)        

        self.btn_histo = ttk.Button(self.labFrame1, text="ant histo", command=self.histo_func)
        self.btn_histo.grid(column=4, row=0, sticky=(N, S, E, W), pady=2, padx=2)  
        
        self.btn_filter = ttk.Button(self.labFrame1, text="filter", command=self.filter_func)
        self.btn_filter.grid(column=4, row=1, sticky=(N, S, E, W), pady=2, padx=2)        
        
        self.btn_compare = ttk.Button(self.labFrame1, text="compare", command=self.compare_func)
        self.btn_compare.grid(column=3, row=1, sticky=(N, S, E, W), pady=2, padx=2)
        
        self.var_btn_custom1 = tkinter.StringVar()
        if tomcat_running():
            self.var_btn_custom1.set("stop tomcat")
        else:
            self.var_btn_custom1.set("start tomcat")                      
        self.btn_custom1 = ttk.Button(self.labFrame1, textvariable=self.var_btn_custom1, command=self.start_stop_tomcat_func)
        self.btn_custom1.grid(column=1, row=1, sticky=(N, S, E, W), pady=2, padx=2) 

        self.btn_custom2 = ttk.Button(self.labFrame1, text="deploy rgslite", command=self.deploy_tomcat_func)
        self.btn_custom2.grid(column=2, row=1, sticky=(N, S, E, W), pady=2, padx=2) 
        
        self.btn_custom3 = ttk.Button(self.labFrame1, text="build paytables", command=self.build_paytables_func)
        self.btn_custom3.grid(column=0, row=2, sticky=(N, S, E, W), pady=2, padx=2)
        
        self.btn_custom4 = ttk.Button(self.labFrame1, text="update glecomponent", command=self.update_glecomponent_func)
        self.btn_custom4.grid(column=1, row=2, sticky=(N, S, E, W), pady=2, padx=2)        
        
        #
        self.btn_custom_2_1 = ttk.Button(self.labFrame2, text="custom_2_1", command=self.custom3_func)
        self.btn_custom_2_1.grid(column=0, row=0, sticky=(N, S, E, W), pady=2, padx=2)
        
        self.btn_custom_2_2 = ttk.Button(self.labFrame2, text="custom_2_2", command=self.custom3_func)
        self.btn_custom_2_2.grid(column=1, row=0, sticky=(N, S, E, W), pady=2, padx=2)

        self.btn_custom_2_3 = ttk.Button(self.labFrame2, text="custom_2_3", command=self.custom3_func)
        self.btn_custom_2_3.grid(column=2, row=0, sticky=(N, S, E, W), pady=2, padx=2)
        
        self.btn_custom_2_4 = ttk.Button(self.labFrame2, text="custom_2_4", command=self.custom3_func)
        self.btn_custom_2_4.grid(column=3, row=0, sticky=(N, S, E, W), pady=2, padx=2)
        
        self.btn_custom_2_5 = ttk.Button(self.labFrame2, text="custom_2_5", command=self.custom3_func)
        self.btn_custom_2_5.grid(column=4, row=0, sticky=(N, S, E, W), pady=2, padx=2)        
        
                                               
        # right listbox
        
        self.listBox = Listbox(self.f_rig, background="white", fg="black", selectbackground="blue", highlightcolor="green", selectmode=EXTENDED)
        self.listBox.config(font=("consolas", 8))
        self.listBox.bind('<<ListboxSelect>>', self.onListBoxSelect)
        self.listBox.grid(column=0, row=2, columnspan=3, sticky=(N, S, E, W), pady=0, padx=0)
        
        self.scrolla = Scrollbar(self.f_rig, command=self.listBox.yview)
        self.scrolla.grid(column=3, row=2, sticky=(N, S, E, W))
        self.listBox['yscrollcommand'] = self.scrolla.set
        
        self.btn_open_dir = ttk.Button(self.f_rig, text="open", command=self.openDir_func)
        self.btn_open_dir.grid(column=1, row=0, sticky=(N, S, E, W), pady=0, padx=2)
                
        self.btn_clear_listBox = ttk.Button(self.f_rig, text="clear", command=self.clearListBox_func)
        self.btn_clear_listBox.grid(column=2, row=0, sticky=(N, S, E, W), pady=0, padx=0)
        
        self.lab_listBox = ttk.Label(self.f_rig, text="Id | Action | From | To | File")
        self.lab_listBox.grid(column=0, row=1, sticky=(N, S, E, W), pady=0, padx=0)
 
        # middle text
        self.textCtrl = TextWithMenu(self.f_mid, background="White", borderwidth=3, relief="sunken", fg='blue', selectbackground="yellow", selectforeground="red")
        self.textCtrl.config(font=("consolas", 10), undo=True, wrap='word')
        self.textCtrl.grid(column=0, columnspan=6, row=1, sticky=(N, S, E, W), pady=0, padx=0)
        
        self.scrollb = Scrollbar(self.f_mid, command=self.textCtrl.yview)
        self.scrollb.grid(column=7, row=1, sticky=(N, S, E, W))
        self.textCtrl['yscrollcommand'] = self.scrollb.set
        
        self.var_filter_check = IntVar()
        self.filter_check = Checkbutton(self.f_mid, text="Filter", variable=self.var_filter_check, command=self.filter_check_func)
        self.filter_check.grid(column=0, row=0, sticky=(N, S, E, W))
        
        self.var_filter_check_inc = IntVar()
        self.filter_check_inc = Checkbutton(self.f_mid, text="Filter In", variable=self.var_filter_check_inc, command=self.filter_check_in_func)
        self.filter_check_inc.grid(column=1, row=0, sticky=(N, S, E, W))        
        
        self.text_search = Text(self.f_mid, height=1, width=2)
        self.text_search.grid(column=4, row=0, sticky=(N, S, E, W))
        self.btn_search = ttk.Button(self.f_mid, text="search", command=self.search_func)
        self.btn_search.grid(column=5, row=0, sticky=(N, S, E, W), padx=5)
        
        # bottom
        self.prog_style = ttk.Style()
        self.prog_style.configure('Niklas.Horizontal.TProgressbar', troughcolor="#b2b2b2", background="green",
                                  thickness=5, troughrelief="flat", relief="flat", borderwidth=1)
        self.progLab1 = Label(self.f_bom, background="#334353", foreground="white", font=("consolas", 8), text="build java code:")
        self.progLab1.grid(column=0, row=0, sticky=(N, S, E, W), padx=1, pady=2)        
        self.progBar_bld_pkg_lite = Progressbar(self.f_bom, style='Niklas.Horizontal.TProgressbar', orient=tkinter.HORIZONTAL, length=100, mode="determinate")
        self.progBar_bld_pkg_lite.grid(column=1, row=0, sticky=(N, S, E, W), padx=1, pady=2)
        
        self.progLab1_A = Label(self.f_bom, background="#334353", foreground="white", font=("consolas", 8), text="build paytables:")
        self.progLab1_A.grid(column=2, row=0, sticky=(N, S, E, W), padx=1, pady=2)        
        self.progBar_bld_paytables = Progressbar(self.f_bom, style='Niklas.Horizontal.TProgressbar', orient=tkinter.HORIZONTAL, length=100, mode="determinate")
        self.progBar_bld_paytables.grid(column=3, row=0, sticky=(N, S, E, W), padx=1, pady=2)        
        
        self.progLab2 = Label(self.f_bom, background="#334353", foreground="white", font=("consolas", 8), text="deploy rgslite:")
        self.progLab2.grid(column=4, row=0, sticky=(N, S, E, W), padx=1, pady=2)        
        self.progBar_dpl_lite = Progressbar(self.f_bom, style='Niklas.Horizontal.TProgressbar', orient=tkinter.HORIZONTAL, length=100, mode="determinate")
        self.progBar_dpl_lite.grid(column=5, row=0, sticky=(N, S, E, W), padx=1, pady=2)        

        self.progLab3 = Label(self.f_bom, background="#334353", foreground="white", font=("consolas", 8), text="run histo:")
        self.progLab3.grid(column=6, row=0, sticky=(N, S, E, W), padx=1, pady=2)        
        self.progBar_run_histo = Progressbar(self.f_bom, style='Niklas.Horizontal.TProgressbar', orient=tkinter.HORIZONTAL, length=100, mode="determinate")
        self.progBar_run_histo.grid(column=7, row=0, sticky=(N, S, E, W), padx=1, pady=2)
        
        self.progLab4 = Label(self.f_bom, background="#334353", foreground="white", font=("consolas", 8), text="cust func1:")
        self.progLab4.grid(column=8, row=0, sticky=(N, S, E, W), padx=1, pady=2)        
        self.progBar_cust_1 = Progressbar(self.f_bom, style='Niklas.Horizontal.TProgressbar', orient=tkinter.HORIZONTAL, length=100, mode="determinate")
        self.progBar_cust_1.grid(column=9, row=0, sticky=(N, S, E, W), padx=1, pady=2)         

        self.progLab5 = Label(self.f_bom, background="#334353", foreground="white", font=("consolas", 8), text="cust func2:")
        self.progLab5.grid(column=10, row=0, sticky=(N, S, E, W), padx=1, pady=2)        
        self.progBar_cust_2 = Progressbar(self.f_bom, style='Niklas.Horizontal.TProgressbar', orient=tkinter.HORIZONTAL, length=100, mode="determinate")
        self.progBar_cust_2.grid(column=11, row=0, sticky=(N, S, E, W), padx=1, pady=2)    
                
        # added resizing configs
        
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        
        # f1        
        self.f1.columnconfigure(0, weight=1)
        self.f1.columnconfigure(1, weight=1)
        self.f1.columnconfigure(2, weight=3)
        self.f1.columnconfigure(3, weight=1)
        self.f1.columnconfigure(4, weight=1)
        
        self.f1.rowconfigure(0, weight=1)
        self.f1.rowconfigure(1, weight=80)
        self.f1.rowconfigure(2, weight=80)
        self.f1.rowconfigure(3, weight=1)
        
        # f_top
        self.f_top.rowconfigure(0, weight=1)
        self.f_top.rowconfigure(1, weight=1)
        self.f_top.rowconfigure(2, weight=80)
        self.f_top.rowconfigure(3, weight=80)                
        
        self.f_top.columnconfigure(0, weight=1)
        self.f_top.columnconfigure(1, weight=1)
        self.f_top.columnconfigure(2, weight=1)
        self.f_top.columnconfigure(3, weight=1)
        self.f_top.columnconfigure(4, weight=1)
        self.f_top.columnconfigure(5, weight=10)
        self.f_top.columnconfigure(6, weight=10)
        self.f_top.columnconfigure(7, weight=1)
        self.f_top.columnconfigure(8, weight=1)
        self.f_top.columnconfigure(9, weight=1)
        self.f_top.columnconfigure(10, weight=1)
        self.f_top.columnconfigure(11, weight=1)
        
        # LabFrame-1 
        self.labFrame1.rowconfigure(0, weight=1)
        self.labFrame1.rowconfigure(1, weight=1)
        self.labFrame1.rowconfigure(2, weight=80)
        self.labFrame1.rowconfigure(3, weight=80)

        self.labFrame1.columnconfigure(0, weight=1)
        self.labFrame1.columnconfigure(1, weight=1)
        self.labFrame1.columnconfigure(2, weight=1)
        self.labFrame1.columnconfigure(3, weight=1)
        self.labFrame1.columnconfigure(4, weight=1)
        
        # LabFrame-1 
        self.labFrame2.rowconfigure(0, weight=1)
        self.labFrame2.rowconfigure(1, weight=1)
        self.labFrame2.rowconfigure(2, weight=80)
        self.labFrame2.rowconfigure(3, weight=80)

        self.labFrame2.columnconfigure(0, weight=1)
        self.labFrame2.columnconfigure(1, weight=1)
        self.labFrame2.columnconfigure(2, weight=1)
        self.labFrame2.columnconfigure(3, weight=1)
        self.labFrame2.columnconfigure(4, weight=1)
                        
        # f_bottom        
        self.f_bom.rowconfigure(0, weight=1)      
        self.f_bom.columnconfigure(0, weight=1)            
        self.f_bom.columnconfigure(1, weight=1)
        self.f_bom.columnconfigure(2, weight=1)
        self.f_bom.columnconfigure(3, weight=1)
        self.f_bom.columnconfigure(4, weight=1)
        self.f_bom.columnconfigure(5, weight=1)
        self.f_bom.columnconfigure(6, weight=1)
        self.f_bom.columnconfigure(7, weight=1)
        self.f_bom.columnconfigure(8, weight=1)
        self.f_bom.columnconfigure(9, weight=1)
        self.f_bom.columnconfigure(10, weight=1)
        self.f_bom.columnconfigure(11, weight=1)
        self.f_bom.columnconfigure(12, weight=1)
        self.f_bom.columnconfigure(13, weight=1) 
        self.f_bom.columnconfigure(14, weight=1)
        self.f_bom.columnconfigure(15, weight=1)      
        self.f_bom.columnconfigure(16, weight=1)
        self.f_bom.columnconfigure(17, weight=1)
        self.f_bom.columnconfigure(18, weight=1) 
        self.f_bom.columnconfigure(19, weight=1)
        self.f_bom.columnconfigure(20, weight=1)         
               
        # f_right
        self.f_rig.columnconfigure(0, weight=90)
        self.f_rig.columnconfigure(1, weight=1)
        self.f_rig.columnconfigure(2, weight=1)
        self.f_rig.rowconfigure(0, weight=1)
        self.f_rig.rowconfigure(1, weight=1)
        self.f_rig.rowconfigure(2, weight=90)
        
        # f_middle
        self.f_mid.columnconfigure(0, weight=1)
        self.f_mid.columnconfigure(1, weight=1)
        self.f_mid.columnconfigure(2, weight=1)
        self.f_mid.columnconfigure(3, weight=40)
        self.f_mid.columnconfigure(4, weight=10)
        self.f_mid.columnconfigure(5, weight=1)
        # self.f_mid.columnconfigure(4, weight=1)
                                        
        self.f_mid.rowconfigure(0, weight=1)
        self.f_mid.rowconfigure(1, weight=200)
 
    def get_widget_attributes(self):
        all_widgets = self.f1.winfo_children()
        for widg in all_widgets:
            print('\nWidget Name: {}'.format(widg.winfo_class()))
            keys = widg.keys()
            for key in keys:
                print("Attribute: {:<20}".format(key), end=' ')
                value = widg[key]
                vtype = type(value)
                print('Type: {:<30} Value: {}'.format(str(vtype), value))
    
    def initStat_func(self):
        _session, _tid, _nextStage, _parser = initStat_func()
        self.session = _session
        self.tid = _tid
        self.nextStage = _nextStage
        self.parser = _parser

        if self.var_filter_check.get() == 0 and self.var_filter_check_inc.get() == 0:
            fileName = _parser._fileName
        elif self.var_filter_check.get() == 1:
            origFileName = _parser._fileName 
            tmpName = _parser._fileName[_parser._fileName.rfind("\\") + 1 : ]
            fileName = gem_configs.workStore + "\\" + tmpName.strip()
            
            filter = []
            with open(gem_configs.filterFile, 'r') as doc:
                for line in doc.readlines():
                    newline = line.strip()
                    if len(newline) > 0:
                        filter.append(newline)
                         
            XMLFileFilter(origFileName, fileName, filter)
             
        elif self.var_filter_check_inc.get() == 1:
            origFileName = _parser._fileName 
            tmpName = _parser._fileName[_parser._fileName.rfind("\\") + 1 : ]
            fileName = gem_configs.workStore_inc + "\\" + tmpName.strip()
            
            filter = []
            with open(gem_configs.filterFile_inc, 'r') as doc:
                for line in doc.readlines():
                    newline = line.strip()
                    if len(newline) > 0:
                        filter.append(newline)
                         
            XMLFileFilterInc(origFileName, fileName, filter)
                            
        self.textCtrl.delete(1.0, END)
        self.dispResponse(fileName)
        
        filename = _parser._fileName[ _parser._fileName.rfind("\\") + 1 : ]
        actionString = "initStat | " + _parser.getText("//Stage") + " | " + _parser.getText("//NextStage") + " | " + filename

        self.writeActionRecord(actionString)
        
    def getPayTable_func(self):
        _parser = getPayTable_func()
        self.parser = _parser
        
        if self.var_filter_check.get() == 0 and self.var_filter_check_inc.get() == 0:
            fileName = _parser._fileName
        elif self.var_filter_check.get() == 1:        
            origFileName = _parser._fileName 
            tmpName = _parser._fileName[_parser._fileName.rfind("\\") + 1 : ]
            fileName = gem_configs.workStore + "\\" + tmpName.strip()
            
            filter = []
            with open(gem_configs.filterFile, 'r') as doc:
                for line in doc.readlines():
                    newline = line.strip()
                    if len(newline) > 0:
                        filter.append(newline)
                         
            XMLFileFilter(origFileName, fileName, filter)
            
        elif self.var_filter_check_inc.get() == 1:        
            origFileName = _parser._fileName 
            tmpName = _parser._fileName[_parser._fileName.rfind("\\") + 1 : ]
            fileName = gem_configs.workStore_inc + "\\" + tmpName.strip()
            
            filter = []
            with open(gem_configs.filterFile_inc, 'r') as doc:
                for line in doc.readlines():
                    newline = line.strip()
                    if len(newline) > 0:
                        filter.append(newline)
                         
            XMLFileFilterInc(origFileName, fileName, filter)             
        
        self.textCtrl.delete(1.0, END)
        self.dispResponse(fileName)
        
        filename = _parser._fileName[ _parser._fileName.rfind("\\") + 1 : ]
        actionString = "getPaytable | " + filename

        self.writeActionRecord(actionString)        
            
    def play_func(self):
        if not hasattr(self, 'tid'): 
            messagebox.showinfo("ERROR", "No transaction Id, initStat firstly.")
            raise Exception("No transaction Id, initStat firstly.")
        elif self.tid is None:
            messagebox.showinfo("ERROR", "No transaction Id, initStat firstly.")
            raise Exception("No transaction Id, initStat firstly.")
        else:
            _tid, _nextStage, _parser = play_func(self.session, self.tid, self.nextStage)
            self.tid = _tid
            self.nextStage = _nextStage
            self.parser = _parser
            
            if self.var_filter_check.get() == 0 and self.var_filter_check_inc.get() == 0:
                fileName = _parser._fileName
            elif self.var_filter_check.get() == 1:
                origFileName = _parser._fileName 
                tmpName = _parser._fileName[_parser._fileName.rfind("\\") + 1 : ]
                fileName = gem_configs.workStore + "\\" + tmpName.strip()
                
                filter = []
                with open(gem_configs.filterFile, 'r') as doc:
                    for line in doc.readlines():
                        newline = line.strip()
                        if len(newline) > 0:
                            filter.append(newline)
                             
                XMLFileFilter(origFileName, fileName, filter)
                                
            elif self.var_filter_check_inc.get() == 1:
                origFileName = _parser._fileName 
                tmpName = _parser._fileName[_parser._fileName.rfind("\\") + 1 : ]
                fileName = gem_configs.workStore_inc + "\\" + tmpName.strip()
                
                filter = []
                with open(gem_configs.filterFile_inc, 'r') as doc:
                    for line in doc.readlines():
                        newline = line.strip()
                        if len(newline) > 0:
                            filter.append(newline)
                             
                XMLFileFilterInc(origFileName, fileName, filter)                   
                
            self.textCtrl.delete(1.0, END)
            self.dispResponse(fileName)
            
            filename = _parser._fileName[ _parser._fileName.rfind("\\") + 1 : ]
            actionString = "play | " + _parser.getText("//Stage") + " | " + _parser.getText("//NextStage") + " | " + filename
    
            self.writeActionRecord(actionString) 
         
    def forceTool_func(self):
        webbrowser.get(global_conf.browser).open(force_configs.url)
    
    def build_package_lite_func(self):
        ant_build_social(self.progBar_bld_pkg_lite, self.parent)
    
    def histo_func(self):
        ant_run_histo(self.progBar_run_histo, self.parent);
    
    def filter_func(self):
        filterDialog = MyDialog_V2(self.parent, "Below items (with xpath) will be filter out:")             
        
    def compare_func(self):
        ids = self.listBox.curselection()
        if len(ids) == 2:
            selected = self.listBox.get(ids[0])
            name1 = selected[ selected.rfind("|") + 1 : ]
            
            selected = self.listBox.get(ids[1])
            name2 = selected[ selected.rfind("|") + 1 : ]
                        
            if self.var_filter_check.get() == 0 and self.var_filter_check_inc.get() == 0:
                fileName1 = gem_configs.origStore + "\\" + name1.strip()
                fileName2 = gem_configs.origStore + "\\" + name2.strip()
            elif self.var_filter_check.get() == 1:
                origFileName1 = gem_configs.origStore + "\\" + name1.strip()
                fileName1 = gem_configs.workStore + "\\" + name1.strip()
                origFileName2 = gem_configs.origStore + "\\" + name2.strip()
                fileName2 = gem_configs.workStore + "\\" + name2.strip()                
                
                filter = []
                with open(gem_configs.filterFile, 'r') as doc:
                    for line in doc.readlines():
                        newline = line.strip()
                        if len(newline) > 0:
                            filter.append(newline)
                             
                XMLFileFilter(origFileName1, fileName1, filter)
                XMLFileFilter(origFileName2, fileName2, filter)
            
            elif self.var_filter_check_inc.get() == 1:
                origFileName1 = gem_configs.origStore + "\\" + name1.strip()
                fileName1 = gem_configs.workStore_inc + "\\" + name1.strip()
                origFileName2 = gem_configs.origStore + "\\" + name2.strip()
                fileName2 = gem_configs.workStore_inc + "\\" + name2.strip()                
                
                filter = []
                with open(gem_configs.filterFile_inc, 'r') as doc:
                    for line in doc.readlines():
                        newline = line.strip()
                        if len(newline) > 0:
                            filter.append(newline)
                             
                XMLFileFilterInc(origFileName1, fileName1, filter)
                XMLFileFilterInc(origFileName2, fileName2, filter)                
            
            f1_c = open(fileName1).readlines()
            f2_c = open(fileName2).readlines()
            
            diff = difflib.HtmlDiff(tabsize=0, wrapcolumn=80).make_file(f1_c, f2_c, fileName1, fileName2)
            report = open(global_conf.storage + "\\diff_report.html", 'w')
            report.write(diff)
            report.close()
            
            webbrowser.get(global_conf.browser).open(global_conf.storage + "\\diff_report.html")
            
        else:
            messagebox.showinfo("ERROR", "Only support to select 2 files to compare.")     
            # self.textCtrl.delete(1.0, END)
            # self.dispResponse(fileName)   
    
    def start_stop_tomcat_func(self):
        if tomcat_running():
            try:        
                tomcat_stop()
            finally:
                self.var_btn_custom1.set("start tomcat")
        else:
            try:
                tomcat_start()
            finally:
                self.var_btn_custom1.set("stop tomcat")        
        
    def deploy_tomcat_func(self):
        # self.progBar_dpl_lite.start(50)
        tomcat_deploy(self.progBar_dpl_lite, self.parent)        
        # self.progBar_dpl_lite.stop()
        
    def build_paytables_func(self):
        build_paytables_func(self.progBar_bld_paytables, self.parent)
    
    def update_glecomponent_func(self):
        ant_build_glecomponent(self.progBar_bld_pkg_lite, self.parent);
    
    def openDir_func(self):
        os.system("explorer.exe %s" % gem_configs.workStore + "\\..\\..")
        
    def clearListBox_func(self):
        file = open(gem_configs.workRecord, "w")
        file.close()
        
        for file in os.listdir(global_conf.storage):
            fileName = os.path.join(global_conf.storage, file)
            if fileName.endswith("cfg") or fileName.endswith("log"):
                continue
            try:
                if os.path.isfile(fileName):
                    os.unlink(fileName)
            except Exception as e:
                print(e)
        
        for file in os.listdir(gem_configs.origStore):
            fileName = os.path.join(gem_configs.origStore, file)
            try:
                if os.path.isfile(fileName):
                    os.unlink(fileName)
            except Exception as e:
                print(e)

        for file in os.listdir(gem_configs.workStore):
            fileName = os.path.join(gem_configs.workStore, file)
            try:
                if os.path.isfile(fileName):
                    os.unlink(fileName)
            except Exception as e:
                print(e)
         
        for file in os.listdir(gem_configs.workStore_inc):
            fileName = os.path.join(gem_configs.workStore_inc, file)
            try:
                if os.path.isfile(fileName):
                    os.unlink(fileName)
            except Exception as e:
                print(e)
                                               
        self.listBox.delete(0, END)
        self.textCtrl.delete(1.0, END)       
    
    def dispResponse(self, fileName):
        lineNum = 1
        blackContPos = []
        quoteContPos = []
        colorContMap = {}        
        
        with open(fileName, 'r') as doc:
            for line in doc.readlines():
                self.textCtrl.insert(END, line)
                
                black = []
                p1 = line.find(">")
                p2 = line.find("<", p1 + 1)
                if p1 != -1 and p2 != -1:
                    black.append(str(lineNum) + "." + str(p1 + 1))
                    black.append(str(lineNum) + "." + str(p2)) 
                    blackContPos.append(black)
                
                for key in xml_disp_configs.keys():
                    confColor = []
                    p1 = line.find(key)
                    if (p1 != -1):
                        p2 = p1 + len(key)
                        confColor.append(str(lineNum) + "." + str(p1))
                        confColor.append(str(lineNum) + "." + str(p2))
                        if colorContMap.get(xml_disp_configs.get(key)) is None:                        
                            colorContMap[xml_disp_configs.get(key)] = [confColor, ]
                        else:
                            cont = colorContMap.get(xml_disp_configs.get(key))
                            cont.append(confColor)   
                
                quotes = []
                p1 = 0
                while True:
                    if p1 != 0:
                        p1 += 1
                    p1 = line.find('\"', p1)
                    if (p1 == -1):
                        break;
                    else:
                        quotes.append(p1)
                        
                if len(quotes) > 0:
                    p1 = quotes[::2]
                    p2 = quotes[1::2]
                    idx = 0                
                    while idx < len(p1):
                        _p1 = p1[idx]
                        _p2 = p2[idx]
                        quoteCont = []
                        quoteCont.append(str(lineNum) + "." + str(_p1 + 1))
                        quoteCont.append(str(lineNum) + "." + str(_p2))
                        idx += 1
                        quoteContPos.append(quoteCont)                                        
                                
                lineNum += 1
        
        for pos in blackContPos:        
            self.textCtrl.tag_add("start", pos[0], pos[1])
        self.textCtrl.tag_config("start", foreground="black")
                
        for key in colorContMap.keys():
            for pos in colorContMap.get(key):
                self.textCtrl.tag_add(key, pos[0], pos[1])
            self.textCtrl.tag_config(key, foreground=key)
            
        for pos in quoteContPos:
            self.textCtrl.tag_add("purple", pos[0], pos[1])
        self.textCtrl.tag_config("purple", foreground="purple")        
    
    def writeActionRecord(self, actionString):
        ids = self.listBox.curselection()
        for id in ids:            
            self.listBox.select_clear(id)
        
        count = self.listBox.size()
        actionString = '{:03d} | {}'.format(count, actionString)    
        self.listBox.insert(END, actionString)
        self.listBox.select_set(self.listBox.size() - 1)
        self.listBox.see(END)        
        with open(gem_configs.workRecord, 'a') as doc:
            doc.write(actionString + "\n")    
    
    def onListBoxSelect(self, evt):
        widget = evt.widget
        ids = widget.curselection()
        if len(ids) > 0:
            selected = self.listBox.get(ids[0])
            name = selected[ selected.rfind("|") + 1 : ]
            if self.var_filter_check.get() == 0 and self.var_filter_check_inc.get() == 0:
                fileName = gem_configs.origStore + "\\" + name.strip()
            elif self.var_filter_check.get() == 1:
                origFileName = gem_configs.origStore + "\\" + name.strip()
                fileName = gem_configs.workStore + "\\" + name.strip()
                filter = []
                with open(gem_configs.filterFile, 'r') as doc:
                    for line in doc.readlines():
                        newline = line.strip()
                        if len(newline) > 0:
                            filter.append(newline)
                             
                XMLFileFilter(origFileName, fileName, filter)
                
            elif self.var_filter_check_inc.get() == 1:
                origFileName = gem_configs.origStore + "\\" + name.strip()
                fileName = gem_configs.workStore_inc + "\\" + name.strip()
                filter = []
                with open(gem_configs.filterFile_inc, 'r') as doc:
                    for line in doc.readlines():
                        newline = line.strip()
                        if len(newline) > 0:
                            filter.append(newline)
                             
                XMLFileFilterInc(origFileName, fileName, filter)                
                 
            self.textCtrl.delete(1.0, END)
            self.dispResponse(fileName)
            
    def search_func(self):
        self.textCtrl.tag_remove("search", "1.0", END)
                
        targ = self.text_search.get(1.0, END).strip()        
        self._reserved_pos = []
        
        if len(targ) > 0:
            idx = self.textCtrl.search(targ, "1.0")            
            if idx.find(".") != -1:
                idx = idx[0: idx.find(".")]
                pos0 = idx + str(".0")
                pos1 = idx + str(".100")
                
                self.textCtrl.tag_add("search", pos0, pos1)
                self._reserved_pos.append(pos0)
                
                self.textCtrl.tag_config("search", background="yellow")
                self.textCtrl.see(idx + ".0")                 
                
                newStart = str(int(idx) + 1) + ".0"
                idx = self.textCtrl.search(targ, newStart)
                while idx.find(".") != -1:
                    idx = idx[0: idx.find(".")]
                    pos0 = idx + str(".0")
                    pos1 = idx + str(".100")
                    
                    if pos0 in self._reserved_pos:
                        break                    
                    self.textCtrl.tag_add("search", pos0, pos1) 
                    self._reserved_pos.append(pos0)                   
                    newStart = str(int(idx) + 1) + ".0"
                    idx = self.textCtrl.search(targ, newStart)
                
                       
    
    def filter_check_func(self):
        if self.var_filter_check.get() == 1:
            if self.var_filter_check_inc.get() == 1:
                self.var_filter_check_inc.set(0)
    
    def filter_check_in_func(self):
        if self.var_filter_check_inc.get() == 1:
            if self.var_filter_check.get() == 1:
                self.var_filter_check.set(0)
    
    def custom3_func(self):
        max_payout = 0
        for idx in range(0, 100000):
            self.play_func()
            pout = int(self.parser.getText("//Payout"))
            if max_payout < pout:
                max_payout = pout
                tid = self.tid
        print("max: " + str(max_payout) + " tid: " + tid)
    
def main():
    
    if not global_conf.use_proxy:
        disable_proxy_in_env_var()
        disable_ie_proxy()
    
    root = Tk()
    root.title("SmartDev - " + global_conf.softwareId + " - " + global_conf.uniqueid + " - " + global_conf.paytable_dir)
    rw = ResizableWindow(root)
    rw.get_widget_attributes()
    
    with open(gem_configs.workRecord, "r") as doc:
        for line in doc.readlines():
            newline = line.strip()
            if len(newline) == 0:
                pass;
            else:
                rw.listBox.insert(END, newline)                
                rw.listBox.see(END)                                 
    ids = rw.listBox.curselection()
    for id in ids:            
        rw.listBox.select_clear(id)
    rw.listBox.select_set(rw.listBox.size() - 1)
        
    root.mainloop()
    
    if not global_conf.use_proxy:
        enable_ie_proxy()
    
    print("Exit finished!")
 
if __name__ == '__main__':
            
    import os
    
    exist = os.path.exists(gem_configs.origStore)
    if not exist:
        os.makedirs(gem_configs.origStore, exist_ok=True)
    exist = os.path.exists(gem_configs.workStore)
    if not exist:
        os.makedirs(gem_configs.workStore, exist_ok=True)
    exist = os.path.exists(gem_configs.workStore_inc)
    if not exist:
        os.makedirs(gem_configs.workStore_inc, exist_ok=True)
                
    exist = os.path.exists(gem_configs.workRecord)
    if not exist:
        file = open(gem_configs.workRecord, "wt")
        file.close()
    exist = os.path.exists(gem_configs.filterFile)
    if not exist:
        file = open(gem_configs.filterFile, "wt")
        file.close()    
    exist = os.path.exists(gem_configs.filterFile_inc)
    if not exist:
        file = open(gem_configs.filterFile_inc, "wt")
        file.close()
                  
    main()
