import numpy as np

popular_base_utility = 1.0
outside_base_utility = 0.0
delta = 0.999
N = int(-6 / np.log10(delta))
num_sim = 100
num_samples = 10000
tau = 50

mu = -1
xi = 0.99
sigma = 1 - xi