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
output = pd.read_csv('~/y4project/data/output_back_filesremoved.csv', usecols=['kic','numax', 'numax_err'])
output = output.loc[(np.abs(output['numax'] - 75) < 30.0)].reset_index(drop=True)
IDs = [random.choice(output['kic']) for i in range(nstars)] # Select a random number of stars from the file, recording their IDs
#IDs = [10802837,12003742,2283075,4760954,11358669,11521197] # Testing set
Numax = [(output.loc[(output['kic'] == IDs[i])]).iloc[0]['numax'] for i in range(len(IDs))] # Create a list of the numax values corresponding to each ID
Numax_err = [(output.loc[(output['kic'] == IDs[i])]).iloc[0]['numax_err'] for i in range(len(IDs))]


# Read oscillation modes and create array for analysis
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

fit1 = sm1.sampling(data=stan_data, iter=iters_notau, chains=nchains, init=[start for n in range(nchains)])
summ_notau = fit1.stansummary()

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

np.savetxt('no_tau_models.csv', params, delimiter=',')

if print_fit == True:
	with open('fullsumm_notau.txt', 'w') as f:
		f.write(summ_notau)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Resample for model that includes the decay term
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sm2 = pickle.load(open('tau_stan.pkl', 'rb'))

no_tau = pd.read_csv('no_tau_models.csv', names=['kic', 'dnu', 'numax',
					 'epsilon', 'alpha', 'A', 'G', 'phi', 'tau'])

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
         'eps_sig': 0.01,
         'al_sig': 0.01,
         'A_sig': 0.01,
         #'G_sig': 0.65,
         'epsilon': no_tau['epsilon'],
         'alpha': no_tau['alpha'],
         'A': no_tau['A'],
         'G': no_tau['G'],
         'phi': no_tau['phi'],
         'epsA': 0.601,
         'epsB': 0.632,
         'alA': 0.015,
         'alB': 0.32,
         'AA': 0.07,
         'AB': 0.87,
         #'GA': 3.08
         'tau': np.ones([len(IDs)])*10
    }
nchains = 4

fit2 = sm2.sampling(data=stan_data, iter=iters_tau, chains=nchains, init=[start for n in range(nchains)])
summ_tau = fit2.stansummary()

params = np.zeros([len(IDs), 9])

for i in np.arange(0,len(IDs),1):
	params[i] = [IDs[i],
				np.mean(fit2['dnu'], axis=0)[i],
				np.mean(fit2['numax'], axis=0)[i],
				np.mean(fit2['epsilon'], axis=0)[i],
				np.mean(fit2['alpha'], axis=0)[i],
				np.mean(fit2['A'], axis=0)[i],
				np.mean(fit2['G'], axis=0)[i],
				np.mean(fit2['phi'], axis=0)[i],
				np.mean(fit2['tau'], axis=0)[i]]

np.savetxt('tau_models.csv', params, delimiter=',')

if print_fit == True:
	with open('fullsumm_tau.txt', 'w') as f:
		f.write(summ_tau)
