import pickle
from pystan import StanModel

# using the same model as before
code = '''
functions {
    real glitch(real n, real dnu, real numax, real epsilon, real alpha, real A, real G, real phi){
        real nmax = numax/dnu - epsilon;
        return (n + epsilon + alpha/2 * (n-nmax)^2 + 
                A*G/(2*pi()) * sin((2*pi()*(n-nmax))/G + phi)) * dnu;
    }
}
data {
    int N;  //number of stars
    int M; //number of modes
    real n[N, M];
    real freq[N, M];
    real freq_err[N, M];
    real numax_obs[N];
    real numax_err[N];
    real dnu_guess[N];
}
parameters {
    real dnu[N];
    real numax[N];
    real<lower = -2.0*pi(), upper = 2.0*pi()> phi[N];
    //real<lower = 0> A[N];
    real G[N];
    //real<lower = 0> tau[N];
    real epsilon_std[N];
    real<lower=0> eps_std;
    real epsA;
    real epsB;
    real alpha_std[N];
    real<lower=0> al_std;
    real alA;
    real alB;
    real A_std[N];
    real<lower=0> A_err;
    real AA;
    real AB;
    //real G_std[N];
    //real<lower=0> G_err;
    //real GA;
    
}

transformed parameters {
    real epsilon[N];
    real alpha[N];
    real A[N];
    //real G[N];
    for (i in 1:N){
        epsilon[i] = epsilon_std[i] * eps_std + (epsA + epsB * log(dnu[i]));
        alpha[i] = alpha_std[i] * al_std + (alA * (dnu[i])^(-alB));
        A[i] = A_std[i] * A_err + (AA * (dnu[i])^(-AB));
        //G[i] = G_std[i] * G_err + GA;
    }
}

model {
    real mod[M];
    for (i in 1:N){
        for (j in 1:M){
            mod[j] = glitch(n[i,j], dnu[i], numax[i], epsilon[i], alpha[i], A[i], G[i], phi[i]);
            // mod[j] ~ normal(freq[i], freq_err[i]);
        }
        freq[i,:] ~ normal(mod, freq_err[i,:]);
        dnu[i] ~ normal(dnu_guess[i], dnu_guess[i]*0.001);
        //A[i] ~ lognormal(log(0.06*dnu[i]^(-0.88)), 0.4);
    }
    
    //epsilon ~ uniform(-1.0, 2.0);
    //nmax ~ normal(10, 4);
    //alpha ~ lognormal(log(0.015*dnu^(-0.32)), 0.3);
    
    G ~ normal(3.08, 0.65);
    phi ~ normal(1.71, 0.77);
    numax ~ normal(numax_obs, numax_err);
    

    //tau ~ normal(50, 10);
    epsilon_std ~ normal(0, 1);
    eps_std ~ normal(0, 0.5);
    epsA ~ normal(0.601, 0.25);
    epsB ~ normal(0.632, 0.25);
    alpha_std ~ normal(0, 1);
    al_std ~ normal(0, 0.5);    
    alA ~ normal(0.015, 0.005);
    alB ~ normal(0.32, 0.08);
    A_std ~ normal(0, 1);
    A_err ~ normal(0, 0.5);
    AA ~ normal(0.06, 0.02);
    AB ~ normal(0.88, 0.05);
    //G_std ~ normal(0, 1);
    //G_err ~ normal(0.65, 0.5);
    //GA ~ normal(3.08, 0.1);
}
'''
sm = StanModel(model_code=code)

# save it to the file 'model.pkl' for later use
with open('no_tau_stan.pkl', 'wb') as f:
    pickle.dump(sm, f)
