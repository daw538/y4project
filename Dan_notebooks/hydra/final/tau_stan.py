import pickle
from pystan import StanModel

# using the same model as before
code = '''
functions {
    real glitch(real n, real dnu, real numax, real epsilon, real alpha, real A, real G, real phi, real tau){
        real nmax = numax/dnu - epsilon;
        return (n + epsilon + alpha/2 * (n-nmax)^2 + 
                (A*G)/(2*pi()) * sin((2*pi()*(n-nmax))/G + phi) * exp(-(n-nmax)/tau)) * dnu;
    }
}

data {
    int N;                  //number of stars
    int M;                  //number of modes
    real n[N, M];           //radial mode number
    real freq[N, M];        //l=0 frequencies
    real freq_err[N, M];
    real numax_obs[N];
    real numax_err[N];
    real dnu_guess[N];
}

parameters {
    // Normal Parameters
    real<lower=0> dnu[N];
    real<lower=0> numax[N];
    real<lower=0> G[N];
    real<lower=-2.0*pi(), upper=2.0*pi()> phi[N];
    real<lower=0> tau[N];
    
    
    // Hierarchical Parameters
    real eps_std[N];
    real<lower=0> eps_sig;
    real<upper=0.1> epsA;
    real<lower=0> epsB;
    
    real al_std[N];
    real<lower=0> al_sig;
    real<lower=0> alA;
    real<lower=0> alB;
    
    real A_std[N];
    real<lower=0> A_sig;
    real<lower=0> AA;
    real<lower=0> AB;
    
    //real G_std[N];
    //real<lower=0> G_sig;
    //real GA;
    
}

transformed parameters {
    real epsilon[N];
    real alpha[N];
    real A[N];
    //real G[N];
    
    for (i in 1:N){
        epsilon[i] = eps_std[i] * eps_sig + (epsA + epsB * log(dnu[i]));
        alpha[i] = al_std[i] * al_sig + (alA * (dnu[i])^(-alB));
        A[i] = A_std[i] * A_sig + (AA * (dnu[i])^(-AB));
        //G[i] = G_std[i] * G_sig + GA;
    }
}

model {
    real mod[M];
    for (i in 1:N){
        for (j in 1:M){
            mod[j] = glitch(n[i,j], dnu[i], numax[i], epsilon[i], alpha[i], A[i], G[i], phi[i], tau[i]);
        }
        freq[i,:] ~ normal(mod, freq_err[i,:]);
        dnu[i] ~ normal(dnu_guess[i], dnu_guess[i]*0.1);
        numax[i] ~ normal(numax_obs[i], numax_err[i]);
		//A[i] ~ uniform(0.000001, 0.1);
    }
    
	//epsilon ~ uniform(0.001, 1.5);
	//A ~ uniform(0.0001, 0.1);
    G ~ normal(3.08, 0.65);  
    //numax ~ normal(numax_obs, numax_err);
    tau ~ normal(10, 4);
    
    // Hierarchical Parameters
    eps_std ~ normal(0, 1);
    eps_sig ~ normal(0, 0.15);
    epsA ~ normal(0.0, 0.15);
    epsB ~ normal(0.3, 0.15);

    al_std ~ normal(0, 1);
    al_sig ~ normal(0, 0.5);    
    alA ~ normal(0.015, 0.005);
    alB ~ normal(0.32, 0.08);
    
    A_std ~ student_t(8, 0, 1);
    A_sig ~ normal(0, 0.5);
    AA ~ normal(0.06, 0.02);
    AB ~ normal(0.88, 0.05);
    
    //G_std ~ normal(0, 1);
    //G_sig ~ normal(0.65, 0.5);
    //GA ~ normal(3.08, 0.1);
}
'''
sm = StanModel(model_code=code)

# save it to the file 'model.pkl' for later use
with open('tau_stan.pkl', 'wb') as f:
    pickle.dump(sm, f)