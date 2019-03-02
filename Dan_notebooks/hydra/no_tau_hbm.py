import numpy as np
import pandas as pd
import random
import pystan

#random.seed(121)
#output = pd.read_csv('../data/output_1000stars.csv', usecols=range(1,4))
output = pd.read_csv('~/y4project/data/output_back_filesremoved.csv', usecols=['kic','numax', 'numax_err'])
output = output.loc[(np.abs(output['numax'] - 75) < 30.0)].reset_index(drop=True)
# Select a random number of stars from the file, recording their IDs
IDs = [random.choice(output['kic']) for i in range(6)]
IDs = [10802837,12003742,2283075,4760954,11358669,11521197]
# Create a list of the numax values corresponding to each ID
Numax = [(output.loc[(output['kic'] == IDs[i])]).iloc[0]['numax'] for i in range(len(IDs))]
Numax_err = [(output.loc[(output['kic'] == IDs[i])]).iloc[0]['numax_err'] for i in range(len(IDs))]



modesID = [pd.read_csv('~/y4project/data/rgbmodes/modes_'+str(IDs[i])+'.csv', usecols=['f0', 'f0_err', 'A0'])
           for i in np.arange(0,len(IDs),1)]
lenmodes = [len(modesID[i]) for i in range(len(IDs))]
maxmodes = max(lenmodes)
arr_n = np.zeros([len(IDs),maxmodes])
arr_freq = np.zeros([len(IDs),maxmodes])
arr_freqerr = np.zeros([len(IDs),maxmodes])


dnu_avgID = []
for i in np.arange(0,len(IDs),1):
    modesID[i] = modesID[i].sort_values(by=['f0'])
    modesID[i] = modesID[i].set_index(np.arange(0,len(modesID[i]),1))
    modesID[i]['dnu'] = (modesID[i]['f0'].diff(2).shift(-1))/2
    dnu_avg = (np.mean(modesID[i]['dnu']))
    dnu_avgID.append(dnu_avg)
    
    n_min = int(modesID[i]['f0'].min() / dnu_avg)
    n = np.arange(n_min, n_min+len(modesID[i]), 1)
    modesID[i].insert(loc=0, column='n', value=n)
    
    # Loop to ensure all arrays are the same length
    if lenmodes[i] < maxmodes:
        l = lenmodes[i]
        while l < maxmodes:
            newrow = {'n': int(np.max(modesID[i]['n'])+1),
                      'f0': np.max(modesID[i]['f0'])+dnu_avgID[i],
                      'f0_err': 100000}
            modesID[i] = modesID[i].append(newrow, ignore_index=True)
            l += 1
        
    arr_n[i,:] = modesID[i]['n']
    arr_freq[i,:] = modesID[i]['f0']
    arr_freqerr[i,:] = modesID[i]['f0_err']
    
    #display(modesID[i])
    
dnu_avgarr = np.asarray(dnu_avgID)

#Define start parameters
eps = []
for i in range(len(IDs)):
    epsilon1 = np.median((modesID[i].f0 % dnu_avg) / dnu_avg)
    eps.append(epsilon1)
epsilon = np.asarray(eps)

numax_obs = Numax
nmax = numax_obs/dnu_avgarr - epsilon
alpha = 0.015*dnu_avgarr**(-0.32)
A = 0.06*dnu_avgarr**(-0.88) 
G = np.ones([len(IDs)])*3.08
tau = np.ones([len(IDs)])*200
phi = np.ones([len(IDs)])*1.71

import pickle
iterations = int(input("How many iterations would you like to use? " ))
sm = pickle.load(open('no_tau_stan.pkl', 'rb'))

stan_data = {'N': len(IDs),
         'M': maxmodes,
         'n': arr_n, 
         'freq': arr_freq,
         'freq_err': arr_freqerr,
         'numax_obs': Numax,
         'numax_err': Numax_err,
         'dnu_guess': dnu_avgarr
        }
start = {'dnu': dnu_avgarr,
         'numax': Numax,
         'eps_std': 0.01,
         'al_std': 0.01,
         'A_err': 0.01,
         #'G_err': 0.65,
         #'epsilon': epsilon,
         #'alpha': alpha,
         #'A': A,
         'G': G,
         'phi': phi,
         'epsA': 0.601,
         'epsB': 0.632,
         'alA': 0.015,
         'alB': 0.32,
         'AA': 0.06,
         'AB': 0.88,
         #'GA': 3.08
         #'tau': tau
    }
nchains = 4

fit = sm.sampling(data=stan_data, iter=iterations, chains=nchains, init=[start for n in range(nchains)])

print(fit)

params = np.zeros([len(IDs), 8])

for i in np.arange(0,len(IDs),1):
    params[i] = [np.mean(fit['dnu'], axis=0)[i],
           np.mean(fit['numax'], axis=0)[i],
           np.mean(fit['epsilon'], axis=0)[i],
           np.mean(fit['alpha'], axis=0)[i],
           np.mean(fit['A'], axis=0)[i],
           np.mean(fit['G'], axis=0)[i],
           np.mean(fit['phi'], axis=0)[i],
                np.nan]

np.savetxt('no_tau_models.csv', params, delimiter=',')
