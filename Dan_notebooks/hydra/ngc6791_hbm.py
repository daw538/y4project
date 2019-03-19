import numpy as np
import pandas as pd
import random
import pystan

# Define input parameters
nstars = int(input("How many stars would you like to sample? " ))
iters_notau = int(input("How many iterations would you like to use for model without decay? " ))
iters_tau = int(input("How many iterations would you like to use for model with decay? " ))

def fitsummary():
	n = 0
	while n < 1:
		print_fit = raw_input("Would you like to save the fit summary files?: " )
		ayes = ['yes', 'y', 'Yes', 'Y']
		noes = ['no', 'n', 'No', 'N']
		if any(print_fit == i for i in ayes):
			print_fit = True
			n = 1
		elif any(print_fit == i for i in noes):
			print_fit = False
			n = 1
		else:
			print("Invalid input. Please try again.")
	return(print_fit)
    
print_fit = fitsummary()

# Select stars for analysis
output = pd.read_csv('~/y4project/data/NGC6791/output_NGC6791.csv', usecols=['ID','Numax', 'Numax_err'])
IDs = list(output['ID'].iloc[0:nstars].values)
Numax = [(output.loc[(output['ID'] == IDs[i])]).iloc[0]['Numax'] for i in range(len(IDs))] # Create a list of the numax values corresponding to each ID
Numax_err = [(output.loc[(output['ID'] == IDs[i])]).iloc[0]['Numax_err'] for i in range(len(IDs))]


# Read oscillation modes and create array for analysis
modesID = [pd.read_csv('~/y4project/data/NGC6791/modes_'+str(IDs[i])+'.csv', usecols=['f0', 'f0_err', 'A0'])
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
tau = np.ones([len(IDs)])*10.0
phi = (-1.9 + 1.5*np.log(dnu_avgarr))
G = np.ones([len(IDs)])*3.08
epsilon = np.ones([len(IDs)])*0.05
alpha = np.ones([len(IDs)])*0.01
A = np.ones([len(IDs)])*0.03


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Sample for model that excludes the decay term, to
# provide best possible starting values.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pickle
sm1 = pickle.load(open('no_tau_stan.pkl', 'rb'))

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
         'eps_sig': 0.001,
         'al_sig': 0.01,
         'A_sig': 0.0001,
         #'G_err': 0.65,
         'epsilon': epsilon,
         'alpha': alpha,
         'A': A,
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

fit1 = sm1.sampling(data=stan_data, iter=iters_notau, chains=nchains, init=[start for n in range(nchains)])
summ_notau = fit1.stansummary(digits_summary = 3)

params = np.zeros([len(IDs), 9])

for i in np.arange(0,len(IDs),1):
    params[i] = [IDs[i],
				np.mean(fit1['dnu'], axis=0)[i],
				np.mean(fit1['numax'], axis=0)[i],
				np.mean(fit1['epsilon'], axis=0)[i],
				np.mean(fit1['alpha'], axis=0)[i],
				np.mean(fit1['A'], axis=0)[i],
				np.mean(fit1['G'], axis=0)[i],
				np.mean(fit1['phi'], axis=0)[i],
				np.nan]

AA = np.mean(fit1['AA'])
AB = np.mean(fit1['AB'])

np.savetxt('ngc6791_notau.csv', params, delimiter=',')

if print_fit == True:
	with open('ngc6791_summ_notau.txt', 'w') as f:
		f.write(summ_notau)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Resample for model that includes the decay term
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Read in best starting parameters, then find indexes of any stars
# that have unphysical/outlying values. Use these indexes to remove,
# from arrays and data that are parsed into stan for the full run.

no_tau = pd.read_csv('ngc6791_notau.csv', names=['kic', 'dnu', 'numax',
					 'epsilon', 'alpha', 'A', 'G', 'phi', 'tau'])
'''
idxs = no_tau[(no_tau['A']<0.0) | (no_tau['A']>0.1) |
              (no_tau['alpha']<0.0)| (no_tau['epsilon']>1.0)].index

arr_n2 = np.delete(arr_n, [idxs], axis=0)
arr_freq2 = np.delete(arr_freq, [idxs], axis=0)
arr_freqerr2 = np.delete(arr_freqerr, [idxs], axis=0)
Numax2 = np.delete(Numax, [idxs], axis=0)
Numax_err2 = np.delete(Numax_err, [idxs], axis=0)
dnu_avgarr2 = np.delete(dnu_avgarr, [idxs], axis=0)

no_tau = no_tau.drop(no_tau.index[[idxs]])
'''
sm2 = pickle.load(open('tau_stan.pkl', 'rb'))

stan_data = {'N': len(IDs),
         'M': maxmodes,
         'n': arr_n, 
         'freq': arr_freq,
         'freq_err': arr_freqerr,
         'numax_obs': Numax,
         'numax_err': Numax_err,
         'dnu_guess': dnu_avgarr
        }
start = {'dnu': no_tau['dnu'],
         'numax': no_tau['numax'],
         'eps_sig': 0.001,
         'al_sig': 0.01,
         'A_sig': 0.0001,
         #'G_sig': 0.65,
         'epsilon': no_tau['epsilon'],
         'alpha': no_tau['alpha'],
         'A': AA*(no_tau['dnu']**(-AB)),
         'G': no_tau['G'],
         'phi': no_tau['phi'],
         'epsA': np.mean(fit1['epsA']),
         'epsB': np.mean(fit1['epsB']),
         'alA': np.mean(fit1['alA']),
         'alB': np.mean(fit1['alB']),
         'AA': AA,
         'AB': AB,
         #'GA': 3.08
         'tau': tau
    }
nchains = 4

fit2 = sm2.sampling(data=stan_data, iter=iters_tau, chains=nchains, init=[start for n in range(nchains)])
summ_tau = fit2.stansummary(digits_summary = 3)

params = np.zeros([len(no_tau['kic']), 9])

for i in np.arange(0,len(no_tau['kic']),1):
	params[i] = [no_tau['kic'].iloc[i],
				np.mean(fit2['dnu'], axis=0)[i],
				np.mean(fit2['numax'], axis=0)[i],
				np.mean(fit2['epsilon'], axis=0)[i],
				np.mean(fit2['alpha'], axis=0)[i],
				np.mean(fit2['A'], axis=0)[i],
				np.mean(fit2['G'], axis=0)[i],
				np.mean(fit2['phi'], axis=0)[i],
				np.mean(fit2['tau'], axis=0)[i]]

np.savetxt('ngc6791_tau.csv', params, delimiter=',')

if print_fit == True:
	with open('ngc6791_summ_tau.txt', 'w') as f:
		f.write(summ_tau)
