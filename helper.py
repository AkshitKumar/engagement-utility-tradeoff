from parameters import *
import numpy as np

def zero_mean_gumbel(n,m):
    return np.random.gumbel(-np.euler_gamma, 1, (n,m))

def gpd_pdf(x, mu, sigma, xi):
    if xi == 0:
        return 1 / sigma * np.exp(- (x - mu) / sigma)
    elif xi > 0:
        return 1 / sigma * (1 + xi * (x - mu) / sigma) ** (-1 / xi - 1) if x >= mu else 0
    elif xi < 0:
        return 1 / sigma * (1 + xi * (x - mu) / sigma) ** (-1 / xi - 1) if x >= mu and x <= mu - sigma / xi  else 0

def gpd_cdf(x, mu, sigma, xi):
    if xi == 0:
        return 1 - np.exp(- (x - mu) / sigma) if x >= mu else 0
    elif xi > 0:
        return 1 - (1 + xi * (x - mu) / sigma) ** (-1 / xi) if x >= mu else 0
    elif xi < 0:
        if x <= mu - sigma / xi and x >= mu:
            return 1 - (1 + xi * (x - mu) / sigma) ** (-1 / xi)
        elif x < mu:
            return 0
        elif x > mu - sigma / xi:
            return 1
        
def gpd_inverse_cdf(p, mu, sigma, xi):
    if xi == 0:
        return mu - sigma * np.log(1 - p)
    else:
        return mu + (sigma / xi) * ((1 - p) ** -xi - 1)

def sample_gpd(mu, sigma, xi, size=1):
    uniform_samples = np.random.uniform(size=size)
    return gpd_inverse_cdf(uniform_samples, mu, sigma, xi)