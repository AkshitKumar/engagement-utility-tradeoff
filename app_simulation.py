import numpy as np
import matplotlib.pyplot as plt
from helper import *
from parameters import *

def simulate_app(popular_base_utility,outside_base_utility,delta, N, num_sim):
    outside_option = outside_base_utility + zero_mean_gumbel(num_sim, N)
    popular_option_first = popular_base_utility + zero_mean_gumbel(num_sim, N)
    popular_option_second = popular_base_utility + zero_mean_gumbel(num_sim, N)
    popular_option = np.maximum(popular_option_first, popular_option_second)
    user_choice = popular_option > outside_option
    user_utility = np.maximum(outside_option, popular_option)
    engagement_vec = np.sum(user_choice * delta ** np.arange(N), axis=1)
    utility_vec = np.sum(user_utility * delta ** np.arange(N), axis=1)
    engagement = np.mean(engagement_vec) * (1 - delta)
    utility = np.mean(utility_vec) * (1 - delta)
    return engagement, utility


