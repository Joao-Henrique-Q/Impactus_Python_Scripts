import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def bs_call(S, K, r, T, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

def implied_vol_call(price, S, K, r, T):
    f = lambda sigma: bs_call(S, K, r, T, sigma) - price
    return brentq(f, 1e-6, 5)

iv = implied_vol_call(6.5, 100, 100, 0.05, 0.5)
print(iv)
