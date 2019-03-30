# Author: Daniel Williams
import numpy as np
import matplotlib.pyplot as plt

'''
The code in this file follows the exercises explained in the paper by
Hogg et al. (2010), as a means of familiarising myself with statistical
approaches to data analysis. Exercises 1-3 consider the technique of linear
regression: first to a linear then quadratic fit.
'''

data = np.genfromtxt('hoggtutorial.txt', names=True)

#%% EXERCISE 1


ex1 = data[4:20]
Y = np.array(ex1['y']).reshape((len(ex1), 1))
A = np.c_[ np.ones(len(ex1)), ex1['x']]
C = np.diag(ex1['sigy'])

# Matrix notation of below: (A.T * C^-1 * A)^-1 (A.T * C^-1 * Y)
Xa = np.linalg.inv(np.dot(A.T,(np.dot(np.linalg.inv(C),A))))
Xb = np.dot(A.T,(np.dot(np.linalg.inv(C),Y)))
X = np.dot(Xa,Xb)

c = X[0]
m = X[1]
xfit = np.arange(min(ex1['x']), max(ex1['x']))
yfit = xfit*m + c


plt.figure(1, figsize=(5,5))
plt.errorbar(ex1['x'], ex1['y'],  yerr=ex1['sigy'], fmt='o')
plt.plot(xfit, yfit)
plt.xlim(0,300)
plt.ylim(0,700)

print(X)
#%% EXERCISE 2

ex2 = data
Y = np.array(ex2['y']).reshape((len(ex2), 1))
A = np.c_[ np.ones(len(ex2)), ex2['x']]
C = np.diag(ex2['sigy'])

# Matrix notation of below: (A.T * C^-1 * A)^-1 (A.T * C^-1 * Y)
Xa = np.linalg.inv(np.dot(A.T,(np.dot(np.linalg.inv(C),A))))
Xb = np.dot(A.T,(np.dot(np.linalg.inv(C),Y)))
X = np.dot(Xa,Xb)

c = X[0]
m = X[1]
xfit = np.arange(min(ex2['x']), max(ex2['x']))
yfit = xfit*m + c


plt.figure(2, figsize=(5,5))
plt.errorbar(ex2['x'], ex2['y'],  yerr=ex2['sigy'], fmt='o')
plt.plot(xfit, yfit)
plt.xlim(0,300)
plt.ylim(0,700)

print('m = ' + str(m))
print('c = ' + c)

#%% EXERCISE 3
ex3 = data[4:20]
Y = np.array(ex3['y']).reshape((len(ex3), 1))
A = np.c_[ np.ones(len(ex3)), ex3['x'], (ex3['x'])**2]
C = np.diag(ex3['sigy'])

# Matrix notation of below: (A.T * C^-1 * A)^-1 (A.T * C^-1 * Y)
Xa = np.linalg.inv(np.dot(A.T,(np.dot(np.linalg.inv(C),A))))
Xb = np.dot(A.T,(np.dot(np.linalg.inv(C),Y)))
X = np.dot(Xa,Xb)

c = X[0]
m = X[1]
q = X[2]

xfit = np.arange(min(ex3['x']), max(ex3['x']))
yfit = q*xfit**2 + xfit*m + c


plt.figure(3, figsize=(5,5))
plt.errorbar(ex3['x'], ex3['y'],  yerr=ex3['sigy'], fmt='o')
plt.plot(xfit, yfit)
plt.xlim(0,300)
plt.ylim(0,700)

print(X)