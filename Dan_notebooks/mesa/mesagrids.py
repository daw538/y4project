#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 18:30:05 2019

@author: daniel
"""

import datetime
#import subprocess
import os
import numpy as np

def inlist_maker(device_values):
    with open('inlist_project_base.f90') as t:
        base_text = t.read()
    for key, val in device_values.items():
        base_text = base_text.replace(key, val)
    return base_text

Zsun = 0.0122
FeHs = np.array([-1.2, -0.6, -0.3, -0.15, 0.0, 0.15])
Zinit = Zsun * 10**FeHs


mass = ['0.8', '1.0', '1.2', '1.4', '1.6', '1.8']
helium = ['0.24', '0.26', '0.28', '0.32', '0.36', '0.40']
metals = [str('{0:+.2f}'.format(i)) for i in FeHs]
Zinits = [str('{0:.6f}'.format(i)) for i in Zinit]
now = datetime.datetime.now()
date = str('{0:%m}{0:%d}'.format(now))


for i in mass:
    for j in helium:
        for k, l in zip(metals, Zinits):
            folder = ('m'+i.replace(".", "")+
                      'y'+j.replace(".", "")+
                      'z'+k.replace(".", ""))
            variables = {
                'xxx': i,
                'zzz': j,
                'uuu': k,
                'vvv': l,
                'mmdd': date,
                'folder': folder
            }
            output = inlist_maker(variables)
            with open('inlist_project', 'w') as f:
                f.write(output)
            os.system('./clean')
            os.system('./mk')
            os.system('./rn')


    

