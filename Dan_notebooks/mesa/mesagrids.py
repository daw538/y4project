#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 18:30:05 2019

@author: daniel
"""

import datetime
import subprocess
import os

def inlist_maker(device_values):
    with open('inlist_project_base.f90') as t:
        base_text = t.read()
    for key, val in device_values.items():
        base_text = base_text.replace(key, val)
    return base_text

mass = ['1.0', '1.2']
helium = ['0.24', '0.40']
#mass = '0.9'
#helium = '0.24'
now = datetime.datetime.now()
date = str('{0:%m}{0:%d}'.format(now))


for i in mass:
    for j in helium:
        folder = 'm'+i.replace(".", "")+'y'+j.replace(".", "")
        variables = {
            'xxx': i,
            'zzz': j,
            'mmdd': date,
            'folder': folder
        }
        output = inlist_maker(variables)
        with open('inlist_project', 'w') as f:
            f.write(output)
        os.system('./clean')
        os.system('./mk')
        os.system('./rn')


    

