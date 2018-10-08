#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Yiz56865
'''
__author__ = 'marsrambler'

from com.config.config_game import gem_configs, xml_disp_configs, paytable_headers
from com.config.config_game import initStat_url, initStat_querystring, initStat_headers
from com.config.config_game import play_url, play_querystring, play_payload, play_payload_picker, play_headers
from com.config.config_game import paytable_url, paytable_querystring, paytable_headers
from com.config.config_game import force_path
from com.config.config_core import toDict

gem_configs = toDict(gem_configs)
xml_disp_configs = toDict(xml_disp_configs)

_initStat_url = toDict(initStat_url)
_initStat_qry = toDict(initStat_querystring)
_initStat_hdr = toDict(initStat_headers)

_initStat_configs = {
                    'url': _initStat_url.url,
                    'querystring': _initStat_qry,
                    'headers': _initStat_hdr
                }

initStat_configs = toDict(_initStat_configs)

_paytable_url = toDict(paytable_url)
_paytable_qry = toDict(paytable_querystring)
_paytable_hdr = toDict(paytable_headers)

_paytable_configs = {
                     'url': _paytable_url.url,
                     'querystring': _paytable_qry,
                     'headers': _paytable_hdr
                }

paytable_configs = toDict(_paytable_configs)

_play_url = toDict(play_url)
_play_querystring = toDict(play_querystring)
_play_payload = toDict(play_payload)
_play_payload_picker = toDict(play_payload_picker)
_play_headers = toDict(play_headers)

_play_configs = {
                 'url' : _play_url.url,
                 'querystring': _play_querystring,
                 'payload': _play_payload.payload,
                 'payload_picker': _play_payload_picker,
                 'headers': _play_headers
                 }

play_configs = toDict(_play_configs) 

force_configs = toDict(force_path)