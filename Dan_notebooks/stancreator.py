import pickle
from pystan import StanModel

# using the same model as before
code = '''
data {
    int N;  //number of stars
    int M; //number of modes
    real n[N, M];
    real freq[N, M];
    real freq_err[N, M];
    real dnu_guess[N];
}
parameters {
    real dnu[N];
    real nmax[N];
    real epsilon[N];
    real alpha[N];
    real<lower = 0> A[N];
    real<lower = 0> G[N];
    real<lower = -2.0*pi(), upper = 2.0*pi()> phi[N];
    real<lower = 0> tau[N];
    real epsA;
    real epsB;
    real alA;
    real alB;
    real AA;
    real AB;
    
}


model {
    real mod[M];
    for (i in 1:N){
        for (j in 1:M){
            mod[j] = (n[i,j] + epsilon[i] + (alpha[i]/2) * (nmax[i] - n[i,j])^2 + 
                A[i]*G[i]/(2*pi()) * sin((2*pi()*(n[i,j]-nmax[i]))/G[i] + phi[i]))*dnu[i]*
                exp(-n[i,j]/tau[i]);
            mod[j] ~ normal(freq[i], freq_err[i]);
        }
        dnu[i] ~ normal(dnu_guess[i], dnu_guess[i]*0.001);
        epsilon[i] ~ normal(epsA + epsB*log(dnu[i]), 0.5);
        alpha[i] ~ lognormal(log(alA*dnu[i]^(-alB)), 0.3);
        A[i] ~ lognormal(log(AA*dnu[i]^(-AB)), 0.4);
    }
    
    //epsilon ~ uniform(-1.0, 2.0);
    nmax ~ normal(10, 4);
    //alpha ~ lognormal(log(0.015*dnu^(-0.32)), 0.3);
    //A ~ lognormal(log(0.06*dnu^(-0.88)), 0.4);
    
    G ~ normal(3.08, 0.65);
    tau ~ normal(50, 10);
    epsA ~ normal(0.601, 0.080);
    epsB ~ normal(0.632, 0.080);
    alA ~ normal(0.015, 0.005);
    alB ~ normal(0.32, 0.08);
    AA ~ normal(0.06, 0.01);
    AB ~ normal(0.88, 0.05);
}
'''
sm = StanModel(model_code=code)

# save it to the file 'model.pkl' for later use
with open('stan.pkl', 'wb') as f:
    pickle.dump(sm, f)
