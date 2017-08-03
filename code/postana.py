# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 16:14:12 2017

@author: admin
"""
import pandas as pd
import numpy as np
spes=['com','equ','fix']
real=dict()
pdt=dict()
diff=dict()

def load_real(spe):
    pass
def load_pdt(name):
    pass

for spe in spes:
    real[spe]=load_real(spes)
    pass
for cst in [0,1]:
    for lag in [1,2]:
        for spe in spes:
            for win_w in [6,12,18,24]:
                name=f"{spe}_{win_w}_{lag}_{cst}"
                pdt[name]=load_pdt(name)
                diff[name]=pdt[name]-real[spe]
                diff[name].dropna(how="any")
                nv=diff[name]
                nv=np.array(nv[nv.columns[0]])
                std=nv.std()
                mean=nv.mean()
                print(name,",",std,",",mean)
    
