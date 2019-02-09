import os
import pandas as pd
import glob

def gyre_inlist(device_values):
        with open('gyre_base.in.f90') as t:
            base_text = t.read()
        for key, val in device_values.items():
            base_text = base_text.replace(key, val)
        return base_text        


folders = os.listdir('LOGS')
files = [glob.glob('LOGS/' + i + '/*.index') for i in folders]


for i,k in zip(files, folders):
    #f = str(i).replace("[","").replace("]","")
    df = pd.read_csv(i[0], skiprows=1, delim_whitespace=True, names=['model','priority','profile'])
    prof1 = df.loc[(df.priority == 1)]['profile'].min()
    prof2 = df.loc[(df.priority == 1)]['profile'].max()
    profiles = [prof1, prof2] 
    
    print(k)
    
    star = str(i[0][13:28])
    
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
        os.system('$GYRE_DIR/bin/gyre gyre.in')
      