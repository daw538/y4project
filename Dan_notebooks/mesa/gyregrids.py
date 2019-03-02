import os
import pandas as pd
import glob
import time


def gyre_inlist(device_values):
        with open('gyre_base.in.f90') as t:
            base_text = t.read()
        for key, val in device_values.items():
            base_text = base_text.replace(key, val)
        return base_text        


folders = os.listdir('LOGS')
files = [glob.glob('LOGS/' + i + '/*.index') for i in folders]


for i,k in zip(files, folders):
    df = pd.read_csv(i[0], skiprows=1, delim_whitespace=True, names=['model','priority','profile'])
    profiles = df.loc[(df.priority == 1)]['profile'].values
    
    #star = str(i[0][13:33])
    star = str(i[0][18:40])
    
    print(star)
    for j in profiles:
        variables = {
            'NNN': str(j),
            'folder': str(k),
            'modelname': star
        }
        
        output = gyre_inlist(variables)
        #print(output)
        #input("Press Enter to continue...")
        with open('gyre.in', 'w') as f:
            f.write(output)
        #time.sleep(1.0)   
        os.system('$GYRE_DIR/bin/gyre gyre.in')
    
