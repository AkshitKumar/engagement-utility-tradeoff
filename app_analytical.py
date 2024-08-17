import numpy as np
import scipy.integrate as spi
from parameters import *
from helper import *

def app(popular_base_utility, outside_base_utility):
    engagement = 2 * np.exp(popular_base_utility) / (np.exp(outside_base_utility) + 2 * np.exp(popular_base_utility))
    utility = np.log(np.exp(outside_base_utility) + 2 * np.exp(popular_base_utility))
    return engagement, utility