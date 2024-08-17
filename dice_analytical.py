import numpy as np
import scipy.integrate as spi
from parameters import *
from helper import *
from app_analytical import app

ub = 700
v = popular_base_utility
o = outside_base_utility


def dice(v,o,mu,sigma,xi,delta,tau):
    # compute the expected engagement and welfare till time tau by showing one popular and one niche item
    experimentation_engagement_integrand = lambda x: (1 - np.exp(o) / (np.exp(o) + np.exp(v) +  np.exp(x))) * gpd_pdf(x,mu,sigma,xi)
    experimentation_engagement_integrand_approx = lambda x: gpd_pdf(x,mu,sigma,xi)
    experimentation_welfare_integrand = lambda x: np.log(np.exp(o) + np.exp(v) + np.exp(x)) * gpd_pdf(x,mu,sigma,xi)
    experimentation_welfare_integrand_approx = lambda x: x * gpd_pdf(x,mu,sigma,xi)
    experimentation_engagement = spi.quad(experimentation_engagement_integrand, mu, ub)[0] + spi.quad(experimentation_engagement_integrand_approx, ub, np.inf)[0]
    experimentation_welfare = spi.quad(experimentation_welfare_integrand, mu, ub)[0] + spi.quad(experimentation_welfare_integrand_approx, ub, np.inf)[0]

    # compute the expected engagement and welfare after time tau by showing the popular item to all the users with attraction parameter less than the popular type
    both_niche_engagement_integrand = lambda x: (1 - np.exp(o) / (np.exp(o) + 2 * np.exp(x))) * gpd_pdf(x,mu,sigma,xi)
    both_niche_engagement_integrand_approx = lambda x: gpd_pdf(x,mu,sigma,xi)
    both_niche_welfare_integrand = lambda x: np.log(np.exp(o) + 2 * np.exp(x)) * gpd_pdf(x,mu,sigma,xi)
    both_niche_welfare_integrand_approx = lambda x: (x + np.log(2)) * gpd_pdf(x,mu,sigma,xi)
    both_niche_engagement = spi.quad(both_niche_engagement_integrand, v, ub)[0] + spi.quad(both_niche_engagement_integrand_approx, ub, np.inf)[0]
    both_niche_welfare = spi.quad(both_niche_welfare_integrand, v, ub)[0] + spi.quad(both_niche_welfare_integrand_approx, ub, np.inf)[0]

    # compute the expected engagement and welfare
    engagement = (1 - delta ** tau) * experimentation_engagement + delta ** tau * (both_niche_engagement + app(v,o)[0] * gpd_cdf(v,mu,sigma,xi))
    utility = (1 - delta ** tau) * experimentation_welfare + delta ** tau * (both_niche_welfare + app(v,o)[1] * gpd_cdf(v,mu,sigma,xi))
    return engagement, utility